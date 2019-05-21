import pandas as pd
import numpy as np
import os

# path = ''
#
# df = pd.read_csv('test1.csv')
# print(df.head())

path1 = (os.getcwd())
print("********")
path2 = os.path.join(path1, 'data')
print(path2)
print("********")

for file in os.listdir('data'):
    print(file)


