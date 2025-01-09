# decompyle3 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.9.1 (tags/v3.9.1:1e5d33e, Dec  7 2020, 17:08:21) [MSC v.1927 64 bit (AMD64)]
# Embedded file name: S7ValueRestore.py
import sys, socket, struct, string, time
from sys import argv
script, IP = argv
hex_dict = {
  'a': 10,
  'b': 11,
  'c': 12,
  'd': 13,
  'e': 14,
  'f': 15}

def xstrip(msg):
    __FILTER = ''.join([' ' if (chr(x) not in string.printable or chr(x) in string.whitespace) else (chr(x)) for x in range(0, 256)])
    return msg.translate(__FILTER)


def hex2int(num):
    if num in hex_dict.keys():
        num = hex_dict[num]
    else:
        num = int(num)
    return num


def datatrans(hex_num):
    d = []
    for i in range(0, len(hex_num) - 1, 2):
        num = 16 * hex2int(hex_num[i]) + hex2int(hex_num[i + 1])
        yield num


def CotpConnect(sock):
    try:
        cotp_header = '0300001611e00000000200c1020101c2020101c0010a'
        req = b''
        for data in datatrans(cotp_header):
            req += struct.pack('!B', data)
        else:
            sock.send(req)

    except socket.error:
        print('Connection refused.')
        sock.close()
        return
    rsp = sock.recv(1024)


def S7Setupcommunication(sock):
    try:
        s7comm_header = '0300001902f08032010000ccc100080000f0000001000103c0'
        req = b''
        for data in datatrans(s7comm_header):
            req += struct.pack('!B', data)
        else:
            sock.send(req)

    except socket.error:
        print('Connection refused.')
        sock.close()
        return
    rsp = sock.recv(1024)


def PLCRestore(sock):
    try:
        s7comm_header = '0300002d02f080320700000ece000c00100001120812480b0000000000ff09000c010110060001000184000720'
        req = b''
        for data in datatrans(s7comm_header):
            req += struct.pack('!B', data)
        else:
            sock.send(req)
            rsp = sock.recv(1024)

    except socket.error:
        print('Connection refused.')
        sock.close()
        return
    sock.close()
    return rsp


def s7_Test(ip, port):
    print('Target PLC Ip Addr : %s\n' % ip)
    print('-------PLC Restoring-------')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        s.connect((ip, port))
    except socket.error as msg:
        try:
            sys.stdout.write('Create socket failed, please check the target controller is online!')
            sys.exit(1)
        finally:
            msg = None
            del msg

    else:
        time.sleep(3)
        CotpConnect(s)
        S7Setupcommunication(s)
        PLCRestore(s)


if __name__ == '__main__':
    s7_Test(argv[1], 102)
# okay decompiling S7ValueRestore.pyc