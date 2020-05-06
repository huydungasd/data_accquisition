import csv
import pandas as pd

filepath = './innovators.csv'
df = pd.read_csv(filepath)

def data_transform(data, sensibility):
    assert data.shape[1] % 2 == 0
    
    data_list = []
    for i in range(int(data.shape[1]/2)):
        data_trans = data.iloc[:, i*2+1] * 2**8 + data.iloc[:, i*2]
        data_trans[data_trans > 32767] -= 65536
        data_trans /= sensibility
        data_list.append(data_trans)
    return pd.concat(data_list, axis=1)

time = df.iloc[:, 0]
acc_raw = df.iloc[:, 1:7]
mag_raw = df.iloc[:, 7:13]
gyr_raw = df.iloc[:, 13:19]
ori_raw = df.iloc[:, 19:25]
quat_raw = df.iloc[:, 25:]

print('Average frequency: {0:.2f} Hz'.format((time.size - 1) / (time.iloc[-1] - time.iloc[0])))

acc = data_transform(acc_raw, 100)
acc.columns = ['acc_x', 'acc_y', 'acc_z']
mag = data_transform(mag_raw, 900)
mag.columns = ['mag_x', 'mag_y', 'mag_z']
gyr = data_transform(gyr_raw, 16)
gyr.columns = ['gyr_x', 'gyr_y', 'gyr_z']
ori = data_transform(ori_raw, 16)
ori.columns = ['ori_x', 'ori_y', 'ori_z']
quat = data_transform(quat_raw, 2**14)
quat.columns = ['q', 'p1', 'p2', 'p3']

data = pd.concat([time, acc, mag, gyr, ori, quat], axis=1)
data.to_csv('./data_transfomed.csv', index=False)