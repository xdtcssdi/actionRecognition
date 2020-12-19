#encoding=utf8
from socket import *
import easygui
import struct
import matplotlib.pyplot as plt
import math
from scipy import signal
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
b, a =signal.butter(8, 0.5, 'lowpass')

# 合成加速度
data = []
# 下标
times = []
pos = 0
# 有几组数据
pack_size = 32
# 一组数据中有几条数据
one_pack_size = 3
# 定义域名和端口号
HOST,PORT ='',553
# 定义缓冲区数量(缓存)
BUFFER_SIZE = one_pack_size * pack_size * 4
# 传输服务器地址和端口
ADDR=(HOST,PORT)

try:
    # 创建服务器套接字 AF_INET:IPv4  UPD:协议
    tcpServerSocket = socket(AF_INET,SOCK_DGRAM)
    # 绑定域名和端口号
    tcpServerSocket.bind(ADDR)

    plt.ion()
    while True:
        # 接收数组，阻塞
        msg, addr = tcpServerSocket.recvfrom(BUFFER_SIZE)
        # 对接收的数据进行解析
        for i in range(0, BUFFER_SIZE, 4*one_pack_size):
            vals = []
            for j in range(one_pack_size):
                val = msg[i + 4*j :i + 4*(j+1)]
                value = struct.unpack("f",val)
                vals.append(value[0])
            v = vals[0]**2+vals[1]**2+vals[2]**2
            # data.append(math.sqrt(v))
            data.append(vals)

        times.extend([pos+i for i in range(pack_size)])
        # print(len(times))
        # print(len(data))
        pos += pack_size 
        ix = times
        # 滤波
        # iy = signal.filtfilt(b,a,data)

        # 画图
        plt.title("Acceleration")
        plt.plot(ix, [item[0] for item in data], color="#DC143C", label="X")
        plt.plot(ix, [item[1] for item in data], color="#FF8C00", label="Y")
        plt.plot(ix, [item[2] for item in data], color="#000000", label="Z")
        plt.xlabel("time")
        plt.ylabel("a")
        plt.pause(0.5)
    plt.ioff()
    plt.show()
except Exception as e:
    print(e)
finally:
    tcpServerSocket.close()