#encoding=utf8
from socket import *
import easygui
import struct
import matplotlib.pyplot as plt
import math
from scipy import signal
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.delete("acc")
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
b, a = signal.butter(8, 0.5, 'lowpass')

# 合成加速度
vals = []
# 下标
times = []
pos = 0
# 有几组数据
pack_size = 32
# 一组数据中有几条数据
one_pack_size = 4
# 定义域名和端口号
HOST,PORT ='',553
# 定义缓冲区数量(缓存)
BUFFER_SIZE = one_pack_size * pack_size * 4
# 传输服务器地址和端口
ADDR=(HOST,PORT)

try:
    while True:
        msg = r.lrange('acc', 0, -1)
        vals = []
        for d in msg:
            value = struct.unpack("f"*one_pack_size * pack_size,d)
            for i in range(0,len(value), one_pack_size):
                vals.append([value[i], value[i+1], value[i+2], value[i+3]])
        vals = sorted(vals, key=lambda x:x[0])
        ix = range(len(vals))
    

        plt.title("Acceleration")
        plt.plot(ix, [item[1] for item in vals], color="#DC143C", label="X")
        plt.plot(ix, [item[2] for item in vals], color="#FF8C00", label="Y")
        plt.plot(ix, [item[3] for item in vals], color="#000000", label="Z")
        
        plt.xlabel("time")
        plt.ylabel("a")
        plt.pause(1)
    plt.ioff()
    plt.show()
except Exception as e:
    print(e)
finally:
    pass