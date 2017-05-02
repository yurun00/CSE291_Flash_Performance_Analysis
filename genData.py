import pandas as pd
import os
import numpy as np
import pickle as pk

folderPath = '.\\data\\modelData\\'
# read write ratio, read write size, queue depth, read write randomness, read write stride
def readData(folderPath):
    files = os.listdir(folderPath)
    d, cols = [], ['wr_ratio', 'wr_size', 'q_dep', 'wr_rnd', 'wr_stride', 'bindwidth', 'throughput', 'latency']
    for f in files:
        filePath = folderPath + f
        with open(filePath) as file:
            file.readline()
            vals = [float(n) for n in file.readline().split()]
            names = [float(n) for n in os.path.splitext(f)[0].split('_')[2:]]
            vals = [names[0], names[1], names[2], names[3], names[4], \
                    vals[-3], vals[-2], vals[-1]]
            d.append(vals)
            # print vals
    df = pd.DataFrame(data = d, columns=cols)
    return df

if __name__ == '__main__':
    df = readData(folderPath)
    msk = np.random.rand(len(df)) < 0.7
    trainData = df[msk]
    testData = df[~msk]
    trainData.to_csv('data\\train.csv')
    testData.to_csv('data\\test.csv')