import shutil, os

base_src = r'D:\Hoc_Ths\IoT\IoT_Nhom5\wokwi\pond001'
for i in range(2, 6):
    pond_id = f'pond{i:03d}'
    dest = os.path.join(r'D:\Hoc_Ths\IoT\IoT_Nhom5\wokwi', pond_id)
    os.makedirs(dest, exist_ok=True)
    
    # sketch.ino
    with open(os.path.join(base_src, 'sketch.ino'), 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('THIET BI: AO NUOI 001 (POND001)', f'THIET BI: AO NUOI {i:03d} ({pond_id.upper()})')
    content = content.replace('const char* DEVICE_ID    = "pond001";', f'const char* DEVICE_ID    = "{pond_id}";')
    with open(os.path.join(dest, 'sketch.ino'), 'w', encoding='utf-8') as f:
        f.write(content)
        
    # diagram.json
    with open(os.path.join(base_src, 'diagram.json'), 'r', encoding='utf-8') as f:
        d_content = f.read()
    d_content = d_content.replace('pond001', pond_id).replace('Ao 1:', f'Ao {i}:')
    with open(os.path.join(dest, 'diagram.json'), 'w', encoding='utf-8') as f:
        f.write(d_content)
        
    # libraries.txt
    shutil.copy(os.path.join(base_src, 'libraries.txt'), os.path.join(dest, 'libraries.txt'))
    print(f'Generated {pond_id} successfully!')

print('Done all 5 Wokwi pond directories!')

