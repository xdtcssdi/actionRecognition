import pandas as pd
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def computeVar(x, y, z, g):
    return np.sqrt(x ** 2 + y ** 2 + z ** 2) - g


fileList = glob.glob('action_windows-test/*.csv')
size = 200
for file in fileList:
    data = pd.read_csv(file).drop(['Unnamed: 0', 'ACC'], axis=1)[['bAZ', 'bAY', 'bAZ']]
    x = data.values[:, 0]
    y = data.values[:, 1]
    z = data.values[:, 2]

    acc = computeVar(x, y, z, 9.8)[:size]

    plt.plot(range(size), acc)

    # 显示低筒过滤之后的波形
    b, a = signal.butter(8, 0.5, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, acc)  # data为要过滤的信号
    #plt.plot(range(size), filtedData)

    # 显示归一化之后的波形
    acc_max = max(filtedData)
    acc_min = min(filtedData)
    regulazation = 9.8 * (filtedData - acc_min) / (acc_max - acc_min)
    #plt.plot(range(size), regulazation)
    plt.show()
