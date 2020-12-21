import numpy as np
import pandas as pd
from attitudeAngle import reset, Update_IMU
from glob import glob


files = glob("D:\\temp\\action_windows-test\\*.csv")
nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
for f in files:
    reset()
    data = pd.DataFrame()  
    df =  pd.read_csv(f)
    for i in range(7):
        ax = df.values[:, 1 + i*6 : 1 + i*6 + 1]
        ay = df.values[:, 2 + i*6 : 1 + i*6 + 2]
        az = df.values[:, 3 + i*6 : 1 + i*6 + 3]
        wx = df.values[:, 4 + i*6 : 1 + i*6 + 4]
        wy = df.values[:, 5 + i*6 : 1 + i*6 + 5]
        wz = df.values[:, 6 + i*6 : 1 + i*6 + 6]
        pitch,roll,yaw = Update_IMU(ax,ay,az,wx,wy,wz)
        
        data = pd.concat([data, pd.DataFrame(pitch, columns=[nodes[i] + 'Pitch'])], axis=1)
        data = pd.concat([data, pd.DataFrame(roll, columns=[nodes[i] + 'Roll'])], axis=1)
        data = pd.concat([data, pd.DataFrame(yaw, columns=[nodes[i] + 'Yaw'])], axis=1)
    
    data.to_csv("D:\\temp\\attitudeAngle_windows\\" +f.split("\\")[-1])