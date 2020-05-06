import csv
import pandas as pd

filepath = './innovators.csv'
df = pd.read_csv(filepath)

time = df.iloc[:, 0]
print(time)