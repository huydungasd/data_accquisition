import csv

from utils import *


raw_files = [name for name in os.listdir(raw_dir) if os.path.isfile(raw_dir + name)]
for name in raw_files:
    filepath = f'./raw_data/{name}'
    df = pd.read_csv(filepath)

    time = df.iloc[:, 0]
    acc_raw = df.iloc[:, 1:7]
    mag_raw = df.iloc[:, 7:13]
    gyr_raw = df.iloc[:, 13:19]
    ori_raw = df.iloc[:, 19:25]
    quat_raw = df.iloc[:, 25:33]
    sensor_ir = df.iloc[:, 33:36]


    print('File {0} : Average frequency: {1:.2f} Hz'.format(name, (time.size - 1) / (time.iloc[-1] - time.iloc[0])))

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
    ir = irread_to_cm(sensor_ir)
    ir.columns = ['A0', 'A1', 'A2']

    data = pd.concat([time, acc, mag, gyr, ori, quat, ir], axis=1)
    data.to_csv(f'./transformed_data/{name}', index=False)