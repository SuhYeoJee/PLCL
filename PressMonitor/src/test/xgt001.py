
def get_xgt_header(cmd_len:int):
    company_id = b"LSIS-XGT".ljust(10, b'\x00')
    plc_info = b'\x00\x00' # client -> server
    cpu_info = b'\xA0' # XGK
    source_of_frame = b'\x33' # client -> server
    invoke_id = b'\x00\x10'
    length = cmd_len.to_bytes(2,'big')
    net_pos = b'\x00'

    a = company_id + plc_info + cpu_info + source_of_frame + invoke_id + length + net_pos
    # a = b''
    # for x in [company_id + plc_info + cpu_info + source_of_frame + invoke_id + length + net_pos]:
    #     a += x[::-1] #little endian
    bcc = f"{sum(a) % 256:02X}".encode('ascii')
    return a + bcc

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
        cmd += (addr_length + addr.encode('ascii'))
    # return cmd

    a = b''
    for x in [op + data_type + block_length]:
        a += x[::-1] #little endian
    for addr in addrs:
        addr_length = len(addr).to_bytes(2,'little')
        a += (addr_length + addr.encode('ascii')[::-1])
    return a

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
print(t())
b'LSIS-XGT\x00\x00\x00\x00\xa03\x00\x10\x00\x11\x004F\x00T\x00\x02\x00\x00\x00\x01\x00\x07%DW5004'
b'LSIS-XGT\x00\x00\x00\x00\xa03\x00\x10\x00\x11\x004F\x01\x00\x00\x00\x02\x00T\x00\x07\x004005WD%'
###############################################