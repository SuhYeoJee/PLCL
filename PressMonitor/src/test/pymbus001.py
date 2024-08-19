from pymodbus.client.tcp import ModbusTcpClient

# Modbus 서버의 IP 주소와 포트 설정
MODBUS_SERVER_IP = '192.168.0.50'  # Modbus 서버 IP 주소
MODBUS_PORT = 502  # 일반적인 Modbus TCP 포트

# 읽어올 주소 설정 (DW5004 주소, 예를 들어 40004로 가정)
ADDRESS = 5004  # 주소 (DW5004라고 했지만 실제 주소는 서버에 따라 다를 수 있음)

# Modbus TCP 클라이언트 생성 및 서버에 연결
client = ModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_PORT)

# 서버에 연결 확인
if not client.connect():
    print("서버에 연결할 수 없습니다.")
else:
    try:
        # 주소에서 데이터 읽기 (예: Holding Register)
        result = client.read_holding_registers(ADDRESS, 1)
        
        if result.isError():
            print(f"데이터를 읽는 중 오류 발생: {result}")
        else:
            # 읽어온 값 출력
            print(f"주소 {ADDRESS}의 값: {result.registers[0]}")
    
    finally:
        # 클라이언트 연결 종료
        client.close()