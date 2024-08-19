import socket
import struct

HOST = '192.168.0.50'  # PLC의 IP 주소
PORT = 502  # Modbus TCP 표준 포트

# Modbus TCP 요청 메시지 구성
transaction_id = 0  # 트랜잭션 ID (임의로 설정 가능)
protocol_id = 0  # 프로토콜 ID (Modbus TCP의 경우 0)
length = 6  # 길이 (유닛 ID, 함수 코드, 시작 주소, 레지스터 수 의 바이트 합)
unit_id = 255  # 유닛 ID (Modbus 장치 ID, 1 바이트)
function_code = 4  # 함수 코드 (4는 입력 레지스터 읽기, 1 바이트)
start_address = 0  # 시작 주소 (0부터 시작 , 2 바이트)
register_count = 7  # 읽을 레지스터 수 (7개의 레지스터 읽기 , 2 바이트)

# '>HHHBBHH' 형식 문자열을 사용하여 Modbus 요청 메시지 패킹
request = struct.pack('>HHHBBHH', transaction_id, protocol_id, length, unit_id, function_code, start_address, register_count)

# TCP 소켓 생성 및 연결
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # PLC에 연결
    client_socket.sendall(request)  # 요청 메시지 전송

    # 응답 메시지 받기
    response = client_socket.recv(1024)  # PLC로부터의 응답 받기

# Modbus TCP 응답 메시지 분석
# '>HHHBBB' 형식 문자열을 사용하여 응답 메시지의 헤더 부분 언패킹
response_header = struct.unpack('>HHHBBB', response[:9])
# 나머지 부분을 언패킹하여 레지스터 값들 추출
register_values = struct.unpack('>' + 'H' * register_count, response[9:])

# 결과 출력
print("receive : ", response)  # 받은 전체 응답 메시지
print("header : ", response_header)  # 응답 메시지의 헤더 부분
print("Register values :", register_values)  # 추출된 레지스터 값들
