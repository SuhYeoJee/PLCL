
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

###############################################
# print(get_xgt_cmd())
b'\x01\x00\x00\x00\x02\x00T\x00\x06\x004005WD'
b'\x00T\x00\x02\x00\x00\x00\x01\x00\x07%DW5004'
# print(get_xgt_header(10))
b'LSIS-XGT\x00\x00\x00\x00\xa03\x00\x10\x00\x11\x004F'
s = t().hex()
# print(' '.join(s[i:i+2] for i in range(0, len(s), 2)))
print(s)


b'LSIS-XGT\x00\x00\x00\x00\xa03\x00\x10\x00\x11\x004F\x00T\x00\x02\x00\x00\x00\x01\x00\x07%DW5004'
b'LSIS-XGT\x00\x00\x00\x00\xa03\x00\x10\x00\x11\x004F\x01\x00\x00\x00\x02\x00T\x00\x07\x004005WD%'
###############################################

# 4c 53 49 53 2d 58 47 54 00 00 00 00 a0 33 00 10 00 11 00 34 46 01 00 00 00 02 00 54 00 07 00 34 30 30 35 57 44 25

# 4c 53 49 53 2d 58 47 54 00 00 00 00 a0 33 00 10 00 11 00 34 46 00 54 00 02 00 00 00 01 00 07 25 44 57 35 30 30 34
# 4c 53 49 53 2d 58 47 54 00 00 00 00 b0 33 00 00 11 00 01 50 54 00 02 00 00 00 01 00 07 00 25 44 57 35 30 30 34

# 4c 53 49 53 2d 58 47 54 00 00 00 00 a0 33 00 10 00 12 50 00 54 00 02 00 00 00 01 00 07 00 25 44 57 35 30 30 34 
#                                  00 b0 33 00 00 11 00 01 50 54 00 02 00 00 00 01 00 07 00 25 44 57 35 30 30 34


# company_id = b"LSIS-XGT".ljust(10, b'\x00')
# plc_info = b'\x00\x00' # client -> server
# cpu_info = b'\xA0' # XGK
# source_of_frame = b'\x33' # client -> server
# invoke_id = b'\x00\x10'
# length = cmd_len.to_bytes(2,'big')
# net_pos = b'\x00'
# bcc = f"{sum(a) % 256:02X}".encode('ascii')

# 4c 53 49 53 2d 58 47 54 00 00 
# 00 00 
# b0 
# 33 
# 00 00 
# 11 
# 00 01 
# 50


# 4c 53 49 53 2d 58 47 54 00 00 [company_id]
# 00 00 [plc_info]
# a0 [cpu_info]
# 33 [source_of_frame]
# 00 10 [invoke_id]
# 00 11 [length]
# 00 [net_pos]
# 34 46 [bcc]

# 4c 53 49 53 2d 58 47 54 00 00 
# 00 00 
# a0 33 
# 00 10 
# 00 11 
# 4f 





# op = b'\x00\x54'
# if block_type == 'X': data_type = b'\x00\x00\x00\x00' # BIT
# elif block_type == 'B': data_type = b'\x00\x01\x00\x00' # BYTE
# elif block_type == 'W': data_type = b'\x00\x02\x00\x00' # WORD
# elif block_type == 'D': data_type = b'\x00\x03\x00\x00' # DOUBLE WORD
# elif block_type == 'L': data_type = b'\x00\x04\x00\x00' # LONG WORD
# block_length = len(addrs).to_bytes(2,'big')
# cmd = op + data_type + block_length
# for addr in addrs:
#     addr_length = len(addr).to_bytes(2,'big')
#     cmd += (addr_length + addr.encode('ascii'))


# 00 54
# 00 02 00 00 
# 00 01 
# 00 07 
# 00 25 44 57 35 30 30 34

# 00 54 [op]
# 00 02 00 00[block type]
# 00 01 [block_length]
# 00 07 [addr_length]
# 25 44 57 35 30 30 34 [addr] %DW5004

# 주소 맨앞에 00이 왜들어가는거임

