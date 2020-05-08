import pandas as pd
import numpy as np
import scipy.interpolate


def data_transform(data, sensibility):
    assert data.shape[1] % 2 == 0
    
    data_list = []
    for i in range(int(data.shape[1]/2)):
        data_trans = data.iloc[:, i*2+1] * 2**8 + data.iloc[:, i*2]
        data_trans[data_trans > 32767] -= 65536
        data_trans /= sensibility
        data_list.append(data_trans)
    return pd.concat(data_list, axis=1)

def irread_to_cm(data):
	# Source: https://www.upgradeindustries.com/product/58/Sharp-10-80cm-Infrared-Distance-Sensor-(GP2Y0A21YK0F)
    return (data * 5) ** -1.15 * 27.86

def interpolate_3dvector_linear(input, input_timestamp, output_timestamp):
    assert input.shape[0] == input_timestamp.shape[0]
    func = scipy.interpolate.interp1d(input_timestamp, input, axis=0)
    interpolated = func(output_timestamp)
    return interpolated

def create_imu_data_deep(filepath, frequency=100):
    df = pd.read_csv(filepath)
    df_interp = interpolate_3dvector_linear(df, df.iloc[:, 0], np.arange(df.iloc[0, 0], df.iloc[-1, 0], 0.01))
    df_interp = pd.DataFrame(df_interp, columns=list(df.columns))
    return df_interp.iloc[:, 0:10]