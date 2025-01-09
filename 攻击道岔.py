# Visit https://www.lddgo.net/string/pyc-compile-decompile for more information
# Version : Python 3.7

from ctypes import c_uint16
import snap7
from snap7.exceptions import Snap7Exception
from snap7.util import *

def set_connection_type(self, connection_type):
    '''
    Sets the connection resource type, i.e the way in which the Clients
    connects to a PLC.

    :param connection_type: 1 for PG, 2 for OP, 3 to 10 for S7 Basic
    '''
    result = self.library.Cli_SetConnectionType(self.pointer, c_uint16(connection_type))
    if result != 0:
        raise Snap7Exception('The parameter was invalid')


def write_to_plc(ip, rack, slot, db_number, start_offset, bit, value):
    '''
    向PLC写入数据
    :param ip: PLC的IP地址
    :param rack: PLC的机架号
    :param slot: PLC的插槽号
    :param db_number: DB块号
    :param start_offset: 起始偏移量
    :param bit: 要设置的位
    :param value: 要写入的值，True 或 False
    '''
    client = snap7.client.Client()
    client.set_connection_type(2)
    
    try:
        client.connect(ip, rack, slot)
        if client.get_connected():
            print('连接成功')
            data = client.db_read(db_number, start_offset, 1)
            set_bool(data, 0, bit, value)
            client.db_write(db_number, start_offset, data)
            print(f'''成功将DB{db_number}.DBX{start_offset}.{bit} 设置为 {value}''')
        else:
            print('连接失败')
    except Exception:
        e = None
        
        try:
            print(f'''发生错误: {str(e)}''')
        finally:
            e = None
            del e

    finally:
        client.disconnect()
        client.destroy()


plc_ip = '192.168.1.11'
plc_rack = 0
plc_slot = 1
db_number = 1
start_offset = 34
bit = 4
value = True
write_to_plc(plc_ip, plc_rack, plc_slot, db_number, start_offset, bit, value)
