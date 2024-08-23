import socket
from igzg.utils import write_error

def get_xgt_header(cmd_len:int):
    company_id = b"LSIS-XGT".ljust(10, b'\x00')
    plc_info = b'\x00\x00' # client -> server
    cpu_info = b'\xA0' # XGK
    source_of_frame = b'\x33' # client -> server
    invoke_id = b'\x00\x10'
    length = cmd_len.to_bytes(2,'big')
    # net_pos = b'\x00'

    a = company_id + plc_info + cpu_info + source_of_frame + invoke_id + length # + net_pos
    bcc = (sum(a) & 0xFF).to_bytes(1, 'big')

    header = a + bcc
    return header

def get_xgt_cmd(block_type = "W", addrs=["DW5004"]):
    # single read
    op = b'\x00\x54'
    if block_type == 'X': data_type = b'\x00\x00\x00\x00' # BIT
    elif block_type == 'B': data_type = b'\x00\x01\x00\x00' # BYTE
    elif block_type == 'W': data_type = b'\x00\x02\x00\x00' # WORD
    elif block_type == 'D': data_type = b'\x00\x03\x00\x00' # DOUBLE WORD
    elif block_type == 'L': data_type = b'\x00\x04\x00\x00' # LONG WORD
    block_length = len(addrs).to_bytes(2,'big')
    cmd = op + data_type + block_length
    for addr in addrs:
        addr_length = len(addr).to_bytes(2,'big') 
        cmd += (addr_length + b'\x00' + addr.encode('ascii'))

    return cmd

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
    print(message_dw5004)
    client_socket.sendall(message_dw5004)
    response_dw5004 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
    print("AUTOMATIC_PRGNO: ", response_dw5004.decode('utf-8'))
    print('------------------------------------------')

    # DW2090 주소에 대한 데이터 송신
    message_dw2090 = t('W',['%DW2090'])
    print(message_dw2090)
    client_socket.sendall(message_dw2090)
    response_dw2090 = client_socket.recv(1024)  # 적절한 버퍼 크기 설정
    print("AUTOMATIC_PRGNAME: ", response_dw2090.decode('utf-8'))
    print('------------------------------------------')

except Exception as e:
    write_error(e,console_logging=True)

finally:
    # 소켓 종료
    client_socket.close()
