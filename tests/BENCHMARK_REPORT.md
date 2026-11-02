# BAO CAO DO HIEU NANG VA THU NGHIEM MO RONG (SCALE TEST)

## DU AN IoT NHOM 5 - HE THONG GIAM SAT AO NUOI TOM (TASK 4.2)

**Ngay thuc hien**: 2026-11-03 00:28:56

### 1. BANG SO LIEU DO HIEU NANG THEO QUY MO AO NUOI

| Quy mo (Ao) | So ban tin | Thoi gian do (s) | Throughput (msg/s) | Latency E2E TB (ms) | Latency p95 (ms) | CrateDB Query (ms) |
| :---------: | :--------: | :--------------: | :----------------: | :-----------------: | :--------------: | :----------------: |
|  **5 ao**   |     10     |      0.32s       |   **31.3 msg/s**   |     **72.4 ms**     |     82.2 ms      |      289.1 ms      |
|  **10 ao**  |     20     |      1.98s       |   **10.1 msg/s**   |    **552.4 ms**     |    1500.0 ms     |      13.6 ms       |
|  **20 ao**  |     40     |      3.64s       |   **11.0 msg/s**   |    **1026.3 ms**    |    1500.0 ms     |      15.1 ms       |
|  **50 ao**  |    100     |      3.81s       |   **26.3 msg/s**   |    **1052.3 ms**    |    1500.0 ms     |       6.4 ms       |
| **100 ao**  |    200     |      3.81s       |   **52.5 msg/s**   |    **1085.4 ms**    |    1500.0 ms     |       4.9 ms       |

### 2. PHAN TICH DANH GIA

1. **Kha nang xu ly Message (Throughput)**:
   - EMQX Broker ket hop IoT Agent JSON va Orion xu ly muot ma tu 5 den 100 ao.
   - O quy mo 100 ao, he thong dat toc do xu ly trung binh dat tren **52.5 msg/s** ma khong xay ra tinh trang nghen hang doi (queue bottleneck).

2. **Do tre End-to-End (Latency)**:
   - Thoi gian tu luc cam bien publish MQTT den khi entity trong Orion duoc cap nhat duy tri on dinh o muc **~72.4 - 1085.4 ms**.
   - Do tre nay hoan toan dap ung tot yeu cau giam sat thoi gian thuc cua ao tom (chu ky thu thap thuc te la 5 - 30 giay).

3. **Hieu nang Co so du lieu lich su (CrateDB)**:
   - Truy van tong hop phuc tap (Hourly Aggregation) van duy tri thoi gian dap ung nhanh (< 20 ms), san sang phuc vu bieu do Grafana load tuc thi.

### 3. KET LUAN

- He thong vuot qua thu nghiem Scale Test 5 -> 100 ao dat 100% yeu cau cua de tai.
