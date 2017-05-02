import json
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn import tree
from subprocess import call


wl = ['rd_only', 'wr_only', 'rnd_only', 'seq_only', 'rnd_rd', 'rnd_wr', 'seq_rd', 'seq_wr']
resDir = "results\\wlSpecificModel\\"

def measures(yTest, pred, metric):
    mae = mean_absolute_error(yTest.ix[:, metric], pred[:, metric])
    sse = sum((yTest.ix[:, metric] - pred[:, metric]) ** 2)
    mean = sum(yTest.ix[:, metric]) / len(yTest.ix[:, metric])
    sst = sum((yTest.ix[:, metric] - mean) ** 2)
    r2 = 1-sse/sst
    return mae, r2

def genTree(w, xTrain, yTrain, xTest, yTest):
    if (w == 0): # read only
        xTrainSpec, yTrainSpec = xTrain[xTrain['wr_ratio'] == 0], yTrain[xTrain['wr_ratio'] == 0]
        xTestSpec, yTestSpec = xTest[xTest['wr_ratio'] == 0], yTest[xTest['wr_ratio'] == 0]
    elif (w == 1): # write only
        xTrainSpec, yTrainSpec = xTrain[xTrain['wr_ratio'] == 100], yTrain[xTrain['wr_ratio'] == 100]
        xTestSpec, yTestSpec = xTest[xTest['wr_ratio'] == 100], yTest[xTest['wr_ratio'] == 100]
    elif (w == 2): # random only
        xTrainSpec, yTrainSpec = xTrain[xTrain['wr_rnd'] == 100], yTrain[xTrain['wr_rnd'] == 100]
        xTestSpec, yTestSpec = xTest[xTest['wr_rnd'] == 100], yTest[xTest['wr_rnd'] == 100]
    elif (w == 3): # seqential only
        xTrainSpec, yTrainSpec = xTrain[xTrain['wr_rnd'] == 0], yTrain[xTrain['wr_rnd'] == 0]
        xTestSpec, yTestSpec = xTest[xTest['wr_rnd'] == 0], yTest[xTest['wr_rnd'] == 0]
    elif (w == 4): # random read
        xTrainSpec, yTrainSpec = xTrain[[a == 100 and b == 0 for a,b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]], \
                                    yTrain[[a == 100 and b == 0 for a,b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]]
        xTestSpec, yTestSpec = xTest[[a == 100 and b == 0 for a,b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]], \
                        yTest[[a == 100 and b == 0 for a,b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]]
    elif (w == 5): # random write
        xTrainSpec, yTrainSpec = xTrain[[a == 100 and b == 100 for a, b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]], \
                                 yTrain[[a == 100 and b == 100 for a, b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]]
        xTestSpec, yTestSpec = xTest[[a == 100 and b == 100 for a, b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]], \
                       yTest[[a == 100 and b == 100 for a, b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]]
    elif (w == 6): # sequential read
        xTrainSpec, yTrainSpec = xTrain[[a == 0 and b == 0 for a,b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]], \
                                    yTrain[[a == 0 and b == 0 for a,b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]]
        xTestSpec, yTestSpec = xTest[[a == 0 and b == 0 for a,b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]], \
                        yTest[[a == 0 and b == 0 for a,b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]]
    elif (w == 7): # sequential write
        xTrainSpec, yTrainSpec = xTrain[[a == 0 and b == 100 for a, b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]], \
                                 yTrain[[a == 0 and b == 100 for a, b in zip(xTrain['wr_rnd'], xTrain['wr_ratio'])]]
        xTestSpec, yTestSpec = xTest[[a == 0 and b == 100 for a, b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]], \
                       yTest[[a == 0 and b == 100 for a, b in zip(xTest['wr_rnd'], xTest['wr_ratio'])]]

    # Fit regression model
    regr = DecisionTreeRegressor(max_depth=5)
    regr.fit(xTrainSpec, yTrainSpec)

    # Predict three performance metrics
    pred = regr.predict(xTestSpec)

    metrics = {}
    mae, r2 = measures(yTestSpec, pred, 0)
    metrics['bandwidth'] = {'mae' : mae, 'r2': r2}
    print 'bandwidth:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTestSpec, pred, 1)
    metrics['throughput'] = {'mae': mae, 'r2': r2}
    print 'throughput:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTestSpec, pred, 2)
    metrics['latencys'] = {'mae': mae, 'r2': r2}
    print 'latency:\nmae: ', mae, '\nr2', r2

    fn = 'tree_' + wl[w]
    tree.export_graphviz(regr, out_file=resDir + fn + '.dot', feature_names=xTrain.columns)
    call(['dot', '-Tpng', resDir + fn + '.dot', '-o', resDir + fn + '.png'], shell=True)

    return metrics

if __name__ == '__main__':
    dataTrain = pd.read_csv('data\\train.csv')
    dataTest = pd.read_csv('data\\test.csv')

    xTrain = dataTrain[['wr_ratio', 'wr_size', 'q_dep', 'wr_rnd', 'wr_stride']]
    yTrain = dataTrain[['bindwidth', 'throughput', 'latency']]

    xTest = dataTrain[['wr_ratio', 'wr_size', 'q_dep', 'wr_rnd', 'wr_stride']]
    yTest = dataTrain[['bindwidth', 'throughput', 'latency']]

    metricsData = {};
    for w in range(len(wl)):
        metrics = genTree(w, xTrain, yTrain, xTest, yTest)
        metricsData[wl[w]] = metrics
    md = json.dumps(metricsData)
    with open(resDir + 'metrics.json', 'w') as f:
        f.write(md)