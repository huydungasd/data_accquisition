import os
import csv

from utils.data_processing import *


data_dir = './transformed_data/'
data_files = [name for name in os.listdir(data_dir) if os.path.isfile(data_dir + name)]
for name in data_files:
    # print(name)
    filepath = f'./transformed_data/{name}'
    # df = pd.read_csv(filepath)
    df = create_imu_data_deep(filepath)

    time = df.iloc[:, 0]
    quat_data = df.iloc[:, 13:17]
    sensor_data = df.iloc[:, :10]
    ir_A0 = df.iloc[:, 17]
    ir_A1 = df.iloc[:, 18]
    ir_A2 = df.iloc[:, 19]

    thresshold = 23 # We says the sensor see something if the returned value is less than 22cm
    # Make sure the initial position of Rasp is captured by the IR connected to Arduino's A2 port
    for i in range(10):
        if ir_A2.iloc[i] >= thresshold:
            print(f"Error in file {name} - Initial position error")
            assert ir_A2.iloc[i] < thresshold
    
    # Departure instance
    i_depart = 10
    while ir_A2.iloc[i_depart] < thresshold:
        i_depart += 1
    # Initial distance
    initial_distance = ir_A2.iloc[:i_depart].mean()
    for i in range(1, 6):
        if ir_A2.iloc[i_depart + i] < thresshold and abs(initial_distance - ir_A2.iloc[i_depart + i]) < 2:
            print(f"Error: Review the file {name} - Data of IR A2 line {i_depart + i + 2}")
    
    # Arriving instance
    i_final = time.size - 1
    while ir_A0.iloc[i_final] < thresshold:
        i_final -= 1
    # Final distance
    final_distance = ir_A0.iloc[i_final:].mean()
    for i in range(1, 6):
        if ir_A0.iloc[i_final - i] < thresshold and abs(final_distance - ir_A0.iloc[i_final - i]) < 2:
            print(f"Error: Review the file {name} - Data of IR A0 line {i_final - i + 2}")
    
    # Middle instance
    i_mid_1 = i_depart
    while ir_A1.iloc[i_mid_1] > thresshold:
        i_mid_1 += 1
    i_mid_2 = i_final
    while ir_A1.iloc[i_mid_2] > thresshold:
        i_mid_2 -= 1
    list_tmp = []
    list_ind = []
    for i in range(i_mid_1, i_mid_2 + 1):
        if ir_A1.iloc[i] < thresshold:
            list_tmp.append(i)
        else:
            if len(list_tmp) > len(list_ind):
                list_ind = [*list_tmp]
                list_tmp = []
            print(f"Warning: Review the file {name} - Data of IR A1 line {i + 2}")
        if i == i_mid_2 and len(list_ind) == 0:
            list_ind = [*list_tmp]
    print(f'{name} A1 range: {list_ind[0] + 2} - {list_ind[-1] + 2}')
    i_mid = int((list_ind[0] + list_ind[-1])/2)

    x, y, z = position_calulation( time, i_depart, i_final, h=60, l=140, a0=initial_distance, b0=final_distance, \
                                    t0=time.iloc[i_depart], t1=time.iloc[i_mid], t2=time.iloc[i_final])

    data = pd.concat([time, x, y, z, quat_data], axis=1)
    data.to_csv(f'./data_deep/data1/gt/{name}', index=False)
    sensor_data.to_csv(f'./data_deep/data1/imu/{name}', index=False)
