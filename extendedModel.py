import json
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn import tree
from subprocess import call

resDir = "results\\extendedModel\\"

def measures(yTest, pred, metric):
    mae = mean_absolute_error(yTest.ix[:, metric], pred[:, metric])
    sse = sum((yTest.ix[:, metric] - pred[:, metric]) ** 2)
    mean = sum(yTest.ix[:, metric]) / len(yTest.ix[:, metric])
    sst = sum((yTest.ix[:, metric] - mean) ** 2)
    r2 = 1-sse/sst
    return mae, r2

def genTrees(xTrain, yTrain, xTest, yTest):
    # Fit regression model
    # For bandwidth
    regr1 = DecisionTreeRegressor(max_depth=8)
    regr1.fit(xTrain, yTrain.ix[:, 0])
    # For throughput
    regr2 = DecisionTreeRegressor(max_depth=8)
    regr2.fit(xTrain, yTrain.ix[:, 1])
    # For latency
    regr3 = DecisionTreeRegressor(max_depth=8)
    regr3.fit(xTrain, yTrain.ix[:, 2])

    # Predict three performance metrics
    pred1 = regr1.predict(xTest)
    pred2 = regr2.predict(xTest)
    pred3 = regr3.predict(xTest)
    pred = np.stack((pred1, pred2, pred3), axis = -1)

    metrics = {}
    mae, r2 = measures(yTest, pred, 0)
    metrics['bandwidth'] = {'mae' : mae, 'r2': r2}
    print 'bandwidth:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTest, pred, 1)
    metrics['throughput'] = {'mae': mae, 'r2': r2}
    print 'throughput:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTest, pred, 2)
    metrics['latencys'] = {'mae': mae, 'r2': r2}
    print 'latency:\nmae: ', mae, '\nr2', r2

    tree.export_graphviz(regr1, out_file = resDir + 'tree_bandwidth.dot', feature_names = xTrain.columns)
    call(['dot', '-Tpng', resDir + 'tree_bandwidth.dot', '-o', resDir + 'tree_bandwidth.png'], shell=True)

    tree.export_graphviz(regr2, out_file = resDir + 'tree_throughput.dot', feature_names = xTrain.columns)
    call(['dot', '-Tpng', resDir + 'tree_throughput.dot', '-o', resDir + 'tree_throughput.png'], shell=True)

    tree.export_graphviz(regr1, out_file = resDir + 'tree_latency.dot', feature_names = xTrain.columns)
    call(['dot', '-Tpng', resDir + 'tree_latency.dot', '-o', resDir + 'tree_latency.png'], shell=True)

    return metrics

def genTree(xTrain, yTrain, xTest, yTest):
    # Fit regression model
    regr = DecisionTreeRegressor(max_depth=6)
    regr.fit(xTrain, yTrain)

    # Predict three performance metrics
    pred = regr.predict(xTest)

    metrics = {}
    mae, r2 = measures(yTest, pred, 0)
    metrics['bandwidth'] = {'mae' : mae, 'r2': r2}
    print 'bandwidth:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTest, pred, 1)
    metrics['throughput'] = {'mae': mae, 'r2': r2}
    print 'throughput:\nmae: ', mae, '\nr2', r2

    mae, r2 = measures(yTest, pred, 2)
    metrics['latencys'] = {'mae': mae, 'r2': r2}
    print 'latency:\nmae: ', mae, '\nr2', r2

    tree.export_graphviz(regr, out_file = resDir + 'tree.dot', feature_names = xTrain.columns)
    call(['dot', '-Tpng', resDir + 'tree.dot', '-o', resDir + 'tree.png'], shell=True)

    return metrics

if __name__ == '__main__':
    dataTrain = pd.read_csv('data\\train.csv')
    dataTest = pd.read_csv('data\\test.csv')

    xTrain = dataTrain[['wr_ratio', 'wr_size', 'q_dep', 'wr_rnd', 'wr_stride']]
    yTrain = dataTrain[['bindwidth', 'throughput', 'latency']]

    xTest = dataTrain[['wr_ratio', 'wr_size', 'q_dep', 'wr_rnd', 'wr_stride']]
    yTest = dataTrain[['bindwidth', 'throughput', 'latency']]

    metricsData = genTrees(xTrain, yTrain, xTest, yTest)
    md = json.dumps(metricsData)
    with open(resDir + 'metrics_trees.json', 'w') as f:
        f.write(md)

    metricsData = genTree(xTrain, yTrain, xTest, yTest)
    md = json.dumps(metricsData)
    with open(resDir + 'metrics_tree.json', 'w') as f:
        f.write(md)

    # Plot the results
    '''plt.figure()
    plt.scatter(range(len(yTest)), yTest.ix[:, 0], color="darkorange", label="data")
    plt.scatter(range(len(pred)), pred[:, 0], color="cornflowerblue", label="max_depth=2")
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title("Decision Tree Regression")
    plt.legend()
    plt.show()'''