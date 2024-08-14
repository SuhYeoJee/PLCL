import socket
import time

# 서버의 IP 주소와 포트 설정
SERVER_IP = '192.168.0.50'  # 서버 IP 주소
SERVER_PORT = 2004  # 서버 포트 (적절한 포트로 변경)

# TCP/IP 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 서버에 연결
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Start")
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    

    for i in range(1):
        time.sleep(0.5)

        # DW5004 주소에 대한 데이터 송신
        message_dw5004 = b'\x0500RSS0106%DW5004\x04'
        client_socket.sendall(message_dw5004)
        response_dw5004 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
        print("AUTOMATIC_PRGNO: ", response_dw5004.decode('utf-8'))

        # DW2090 주소에 대한 데이터 송신
        message_dw2090 = b'\x0501RSB06%DW2090\x04'
        client_socket.sendall(message_dw2090)
        response_dw2090 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
        print("AUTOMATIC_PRGNAME: ", response_dw2090.decode('utf-8'))

finally:
    # 소켓 종료
    client_socket.close()


client_socket.sendall(b'\x0501RSS0106%DW5004\x04')
client_socket.recv(1024)
