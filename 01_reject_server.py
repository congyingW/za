import socket
import struct


# 错误的TCP校验和
# 构造一个简单的TCP头部，错误地设置校验和
def create_tcp_header():
    # 源端口、目的端口、序列号、确认号、数据偏移、保留位、标志位、窗口大小
    tcp_header = struct.pack('!HHLLBBHHH', 1234, 80, 0, 0, 5, 0, 0x02, 8192, 0)
    # 错误的校验和，这里只是示例，实际应该正确计算
    tcp_header += struct.pack('!H', 0xFFFF)
    return tcp_header

# 创建IP数据包，这里简化处理，只设置源和目的IP
def create_ip_header():
    return struct.pack('!BBHHHBBH4s4s', 0x45, 0, 0, 0, 0, 0, socket.IPPROTO_TCP, 0, socket.inet_aton("192.168.1.100"), socket.inet_aton("192.168.1.200"))


# TPKT头
def create_tpkt_header(length):
    return struct.pack('!BBB', 3, 0, length)


# COTP头
def create_cotp_header():
    return struct.pack('!BBHHB', 17, 0xf, 0x1000, 0x1000, 0)


# S7Comm头
def create_s7comm_header():
    return struct.pack('!BBHHHHBB', 0x32, 0x01, 0x0000, 0x0001, 0x0000, 0x0000, 0, 0)


# S7Comm参数
def create_s7comm_parameters():
    # 这里以一个简单的读操作参数为例
    return struct.pack('!BBBBBBHHBB3s', 0x04, 0x01, 0x12, 0x01, 0x10, 0x02, 0x0000, 0x0000, 0x84, 0x000000)


# 组合成完整的S7comm协议数据包
def create_s7comm_packet():
    tpkt_length = 17 + 10 + 12
    tpkt_header = create_tpkt_header(tpkt_length)
    cotp_header = create_cotp_header()
    s7comm_header = create_s7comm_header()
    s7comm_parameters = create_s7comm_parameters()
    return tpkt_header + cotp_header + s7comm_header + s7comm_parameters


def send_s7comm_packet():
    packet = create_s7comm_packet()
    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 使用原始套接字发送数据包
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    sock.sendto(packet, ("192.168.1.200", 0))

    try:
        # 连接到PLC，这里假设PLC的IP地址是192.168.1.10，端口是102
        client_socket.connect(("192.168.1.10", 102))
        # 发送数据包
        client_socket.send(packet)
        # 接收响应
        response = client_socket.recv(1024)
        print("Response:", response)
    except Exception as e:
        print("Error:", e)
    finally:
        # 关闭连接
        client_socket.close()


if __name__ == "__main__":
    send_s7comm_packet()

