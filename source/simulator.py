#!/usr/bin/env python3
"""
simulator.py - Gia lap cac ao nuoi tom cho du an (IoT Nhom 5).

Moi ao gui len EMQX, theo quy uoc cua IoT Agent JSON:
    /{apikey}/{device_id}/attrs    {"do":5.4,"ph":7.9,"t":29.1,"s":15.2,"a":"OFF"}
Va nhan lenh suc khi tu:
    /{apikey}/{device_id}/cmd      {"aerator": {"state": "ON"}}  (hoac {"aerator": "ON"})
roi tra ket qua ve:
    /{apikey}/{device_id}/cmdexe   {"aerator": "ON"}
"""
import argparse
import json
import math
import os
import random
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import paho.mqtt.client as mqtt


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


class Pond:
    def __init__(self, idx, apikey, rng, p_anomaly):
        self.device_id = f"pond{idx:03d}"
        self.apikey = apikey
        self.rng = rng
        self.p_anomaly = p_anomaly
        # Moi ao co muc nen hoi khac nhau
        self.do_mean = rng.uniform(5.0, 6.0)      # mg/L
        self.do_amp = rng.uniform(1.4, 2.0)
        self.t_mean = rng.uniform(28.0, 30.0)     # oC
        self.ph_mean = rng.uniform(7.7, 8.1)
        self.sal_mean = rng.uniform(12.0, 20.0)   # ppt
        # Trang thai dong
        self.aerator_on = False
        self.boost = 0.0          # mg/L cong them nho suc khi
        self.anomaly_offset = 0.0
        self.anomaly_left = 0     # so mau con lai cua su kien
        self.anomaly_depth = 0.0

    # ----- topic -----
    @property
    def topic_attrs(self):
        return f"/{self.apikey}/{self.device_id}/attrs"

    @property
    def topic_cmdexe(self):
        return f"/{self.apikey}/{self.device_id}/cmdexe"

    # ----- su kien bat thuong -----
    def start_anomaly(self, depth=None, samples=None):
        self.anomaly_depth = depth if depth is not None else self.rng.uniform(2.0, 3.5)
        self.anomaly_left = samples if samples is not None else self.rng.randint(12, 30)

    # ----- mot mau do -----
    def sample(self, hour):
        """hour: gio gia lap trong ngay, 0..24"""
        r = self.rng
        if self.anomaly_left <= 0 and r.random() < self.p_anomaly:
            self.start_anomaly()
        target_anom = -self.anomaly_depth if self.anomaly_left > 0 else 0.0
        self.anomaly_offset += (target_anom - self.anomaly_offset) * 0.25
        if self.anomaly_left > 0:
            self.anomaly_left -= 1
        # Suc khi: tien dan toi +1.8 mg/L khi bat, ve 0 khi tat
        target_boost = 1.8 if self.aerator_on else 0.0
        self.boost += (target_boost - self.boost) * 0.15

        # DO cao nhat khoang 15h (quang hop), thap nhat khoang 3h sang
        daily = math.sin(2 * math.pi * (hour - 9) / 24)
        do = self.do_mean + self.do_amp * daily + self.boost + self.anomaly_offset + r.gauss(0, 0.08)
        temp = self.t_mean + 2.2 * daily + r.gauss(0, 0.05)
        ph = self.ph_mean + 0.30 * math.sin(2 * math.pi * (hour - 10) / 24) \
            + 0.04 * self.anomaly_offset + r.gauss(0, 0.02)
        sal = self.sal_mean + 0.4 * math.sin(time.time() / 600.0) + r.gauss(0, 0.05)

        return {
            "do": round(_clamp(do, 0.3, 14.0), 2),
            "ph": round(_clamp(ph, 6.5, 9.5), 2),
            "t": round(_clamp(temp, 15.0, 40.0), 2),
            "s": round(_clamp(sal, 0.0, 40.0), 2),
            "a": "ON" if self.aerator_on else "OFF",
        }


def parse_state(value):
    if isinstance(value, dict):
        value = value.get("state", value.get("value", ""))
    return str(value).strip().upper() in ("ON", "1", "TRUE", "START")


def build_client(client_id):
    try:  # paho-mqtt 2.x
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    except AttributeError:  # paho-mqtt 1.x
        return mqtt.Client(client_id=client_id)


def main():
    ap = argparse.ArgumentParser(description="Gia lap ao nuoi tom gui MQTT")
    ap.add_argument("--host", default=os.getenv("MQTT_HOST", "localhost"))
    ap.add_argument("--port", type=int, default=int(os.getenv("MQTT_PORT", "1883")))
    ap.add_argument("--user", default=os.getenv("MQTT_USER"))
    ap.add_argument("--password", default=os.getenv("MQTT_PASSWORD"))
    ap.add_argument("--apikey", default=os.getenv("APIKEY", "shrimpkey"))
    ap.add_argument("--ponds", type=int, default=5, help="so ao (pond001..)")
    ap.add_argument("--interval", type=float, default=5.0, help="chu ky lay mau (giay)")
    ap.add_argument("--day-seconds", type=float, default=600.0,
                    help="mot ngay gia lap keo dai bao nhieu giay")
    ap.add_argument("--qos", type=int, default=1, choices=[0, 1, 2])
    ap.add_argument("--p-anomaly", type=float, default=0.002,
                    help="xac suat moi mau bat dau su kien oxy tut")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--anomaly-pond", default=None, help="ep su kien oxy tut cho ao nay, vi du pond003")
    ap.add_argument("--anomaly-after", type=float, default=30.0, help="sau bao nhieu giay thi ep su kien")
    args = ap.parse_args()

    base_rng = random.Random(args.seed)
    ponds = {}
    for i in range(1, args.ponds + 1):
        p = Pond(i, args.apikey, random.Random(base_rng.random()), args.p_anomaly)
        ponds[p.device_id] = p

    client = build_client(f"shrimp-simulator-{os.getpid()}")
    if args.user:
        client.username_pw_set(args.user, args.password)
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    cmd_filter = f"/{args.apikey}/+/cmd"

    def on_connect(cl, userdata, flags, rc, *extra):
        failed = getattr(rc, "is_failure", None)
        failed = failed if failed is not None else (rc != 0)
        if failed:
            print(f"[mqtt] ket noi that bai: {rc}", file=sys.stderr)
            return
        print(f"[mqtt] da ket noi {args.host}:{args.port}, nhan lenh tai {cmd_filter}")
        cl.subscribe(cmd_filter, qos=1)

    def on_message(cl, userdata, msg):
        parts = msg.topic.strip("/").split("/")
        if len(parts) != 3 or parts[2] != "cmd" or parts[1] not in ponds:
            return
        pond = ponds[parts[1]]
        try:
            body = json.loads(msg.payload.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            print(f"[{pond.device_id}] lenh khong phai JSON: {msg.payload!r}", file=sys.stderr)
            return
        if "aerator" in body:
            pond.aerator_on = parse_state(body["aerator"])
            state = "ON" if pond.aerator_on else "OFF"
            print(f"[{pond.device_id}] nhan lenh suc khi -> {state}")
            cl.publish(pond.topic_cmdexe, json.dumps({"aerator": state}), qos=1)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.host, args.port, keepalive=30)
    client.loop_start()

    print(f"Gia lap {len(ponds)} ao, chu ky {args.interval}s, 1 ngay gia lap = {args.day_seconds}s. Ctrl+C de dung.")
    start = time.time()
    forced = False
    try:
        while True:
            now = time.time()
            hour = ((now % args.day_seconds) / args.day_seconds) * 24.0
            if args.anomaly_pond and not forced and now - start >= args.anomaly_after:
                target = ponds.get(args.anomaly_pond)
                if target:
                    target.start_anomaly(depth=3.0, samples=20)
                    print(f"[{target.device_id}] >>> EP su kien oxy tut <<<")
                forced = True
            for pond in ponds.values():
                data = pond.sample(hour)
                client.publish(pond.topic_attrs, json.dumps(data), qos=args.qos)
                print(f"[{pond.device_id}] h={hour:4.1f} DO={data['do']:5.2f} pH={data['ph']:4.2f} "
                      f"T={data['t']:5.2f} S={data['s']:5.2f} aerator={data['a']}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nDung simulator.")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
