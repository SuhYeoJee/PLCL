def get_xgt_header(cmd_len:int):
    '''
    header                (20)

    CompanyID          (10)
    PLC Info            (2)
    CPU Info            (1)
    Source of Frame     (1)
    Invoke ID           (2)
    Length              (2)
    net_pos             (1)
    BCC                 (1)

    '''

    company_id = b"LSIS-XGT".ljust(10, b'\x00')
    plc_info = b'\x00\x00' # client -> server
    # cpu_info = b'\xA0' # XGK
    cpu_info = b'\xb0' # XGK?
    source_of_frame = b'\x33' # client -> server
    invoke_id = b'\x00\x00'
    length = cmd_len.to_bytes(2,'little')
    # net_pos = b'\x00'
    net_pos = b'\x01' # ?

    a = company_id + plc_info + cpu_info + source_of_frame + invoke_id + length + net_pos
    bcc = (sum(a) & 0xFF).to_bytes(1, 'little')

    header = a + bcc
    return header


def get_xgt_cmd(block_type = "W", addrs=["%DW5004"]):
    '''
    single read     (8 + [2+name])

    op              (2)
    block_type      (2)
    reserve         (2)
    block_length    (2)

    addr_length     (2)
    addr            (name)

    '''    
    # single read
    op = b'\x54\x00' # op = b'\x00\x54'
    if block_type == 'X': data_type = b'\x00\x00\x00\x00' # BIT
    elif block_type == 'B': data_type = b'\x01\x00\x00\x00' # BYTE
    elif block_type == 'W': data_type = b'\x02\x00\x00\x00' # WORD
    elif block_type == 'D': data_type = b'\x03\x00\x00\x00' # DOUBLE WORD
    elif block_type == 'L': data_type = b'\x04\x00\x00\x00' # LONG WORD
    block_length = len(addrs).to_bytes(2,'little')
    cmd = op + data_type + block_length
    for addr in addrs:
        addr_length = len(addr).to_bytes(2,'little') 
        cmd += (addr_length+ addr.encode('ascii'))

    return cmd



cmd = get_xgt_cmd(addrs=['%DW0'])
header = get_xgt_header(len(cmd))

# print(cmd.hex())
# print(header.hex())

print((header + cmd).hex())
