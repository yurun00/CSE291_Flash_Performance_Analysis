import os.path
import re
import matplotlib.pyplot as plt

meas = ['bw', 'iops', 'lat']
feats1 = ['qdep', 'rdsize', 'wr', 'wrsize']
feats2 = ['rdsize_seq', 'rdsize_stride', 'wrsize_seq', 'wrsize_stride']

files = os.listdir('.\\data\\plotData\\')
def fPlot(model, feat, mea):
    fileName = 'model' + `model` + '_' + feat + '_' + mea + '*'
    for fn in files:
        fn = os.path.splitext(fn)[0]
        if re.search(fileName, fn):
            x = range(int(fn.split('_')[-2]), int(fn.split('_')[-1])+1)
            data = []
            with open('.\\data\\plotData\\'+fn+'.data') as file:
                for line in file:
                    data += [float(line)]
            plt.scatter(x, data, marker='.')
            plt.ylabel(mea)
            plt.xlabel(feat)
            plt.savefig('results\\plots\\%s_%s.png' % (feat, mea))
            plt.clf()

if __name__ == '__main__':
    for i in range(0, len(feats1)):
        for j in range(0, len(meas)):
            fPlot(1, feats1[i], meas[j])
    for i in range(0, len(feats2)):
        for j in range(0, len(meas)):
            fPlot(2, feats2[i], meas[j])
