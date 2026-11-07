import paho.mqtt.client as mqtt
import time, requests, json

c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2 if hasattr(mqtt, 'CallbackAPIVersion') else 'probe')
c.connect('broker.emqx.io', 1883, 60)
c.loop_start()

test_payload = json.dumps({"do": 3.45, "ph": 7.85, "t": 28.5, "s": 15.0, "a": "OFF"})
print('Publishing from outside (Wokwi path) to broker.emqx.io...')
c.publish('iot_nhom5_shrimp_c8d2/pond001/attrs', test_payload, qos=1)
time.sleep(2)
c.loop_stop()
c.disconnect()

r = requests.get('http://127.0.0.1:1026/v2/entities/urn:ngsi-ld:Pond:001?options=keyValues', headers={'fiware-service': 'shrimp', 'fiware-servicepath': '/'})
print('Orion response:')
print(json.dumps(r.json(), indent=2))

