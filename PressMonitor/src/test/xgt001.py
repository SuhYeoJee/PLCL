
def read_xgt_header(resp:bytes):
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
    # resp = b'LSIS-XGT\x00\x00\x12\x02\xa0\x11\x00\x00\x0e\x00\x00.U\x00\x02\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00'
    resp_length = int.from_bytes(resp[16:19],'little')
    resp_cmd = resp[20:21+resp_length]
    read_xgt_resp(resp_cmd)
    

def read_xgt_resp(resp_cmd:bytes):
    '''
    single read     (10 + [2+data_length])

    op                          (2)
    block_type                  (2)
    reserve                     (2)
    error_state                 (2)
    error_info/block_length     (2)

    data_length                 (2)
    data                        (data_length)

    '''    
    # resp_cmd = b'U\x00\x02\x00\x00\x00\x00\x00\x01\x00\x02\x00\x00\x00'

    op = resp_cmd[:2]
    block_type = resp_cmd[2:4]
    error_state = resp_cmd[6:8]
    error_info = resp_cmd[8:10]
    block_length = int.from_bytes(resp_cmd[8:10],'little')

    idx = 10
    for i in range(block_length):
        data_length = int.from_bytes(resp_cmd[idx:idx+2],'little')
        data = resp_cmd[idx+2:idx+2+data_length]
        idx = idx+2+data_length
        print(data.hex())

