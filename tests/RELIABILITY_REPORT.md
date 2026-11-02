# BAO CAO THU NGHIEM DO TIN CAY VA PHUC HOI HE THONG (TASK 4.3)
## DU AN IoT NHOM 5 - HE THONG GIAM SAT AO NUOI TOM
**Ngay thuc hien**: 2026-11-03 00:29:58

### 1. BANG KET QUA KIEM THU DO TIN CAY

| Bai test | Noi dung kiem tra | Ket qua mong doi | Thuc te |
|:---|:---|:---|:---:|
| **Test 1: Malformed JSON** | Gui chuoi byte rac len MQTT topic | IoT Agent bo qua an toan, he thong khong crash | **PASSED [OK]** |
| **Test 2: Type Mismatch** | Truyen String vao truong Number (DO, pH) | Tu dong loc loi va tiep nhan binh thuong ban tin hop le sau do | **PASSED [OK]** |
| **Test 3: Fault Isolation** | Mot ao bi loi payload | Cac ao con lai khong bi gian doan, du lieu cach ly tuyet doi | **PASSED [OK]** |
| **Test 4: State Persistence** | Kiem tra Context, Subscriptions va Database | Du lieu khong bi mat, subscriptions duy tri active | **PASSED [OK]** |

### 2. PHAN TICH DO TIN CAY HE THONG

- **Kha nang chong loi du lieu**: IoT Agent for JSON phan tich cu phap payload doc lap, bat ngoai le JSONDecodeError an toan.
- **Kha nang cach ly thiet bi**: Loi tai mot ao bat ky khong anh huong den luong du lieu cua cac ao con lai.
- **Tinh ben vung du lieu**: Nho co MongoDB volume (`mongo-data`) va CrateDB volume (`crate-data`), trang thai thiet bi va lich su du lieu duoc bao toan 100%.
