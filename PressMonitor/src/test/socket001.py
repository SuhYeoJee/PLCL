import socket
from igzg.utils import write_error

from xgt001 import *
from xgt2 import *


def t(block_type = "W", addrs=['%DW5004']):
    cmd = get_xgt_cmd(block_type,addrs)
    header = get_xgt_header(len(cmd))
    return (header + cmd)

# 서버의 IP 주소와 포트 설정
SERVER_IP = '192.168.0.50'  # 서버 IP 주소
SERVER_PORT = 2004  # 서버 포트 (적절한 포트로 변경)

# TCP/IP 소켓 생성
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(10)

try:
    # 서버에 연결
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Start")
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    print('------------------------------------------')

    # DW5004 주소에 대한 데이터 송신
    message_dw5004 = t()
    print(message_dw5004.hex())
    client_socket.sendall(message_dw5004)
    response_dw5004 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
    print(response_dw5004.hex())
    read_xgt_header(response_dw5004)
    print('------------------------------------------')

    # DW2090 주소에 대한 데이터 송신
    message_dw2090 = t('W',['%DW1','%DW2','%DW4'])
    print(message_dw2090.hex())
    client_socket.sendall(message_dw2090)
    response_dw2090 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
    print(response_dw2090.hex())
    read_xgt_header(response_dw2090)
    print('------------------------------------------')

except Exception as e:
    write_error(e,console_logging=True)

finally:
    # 소켓 종료
    client_socket.close()
