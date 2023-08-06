import numpy as np
import csv
import os


def csv2list(filename):
    file = open(os.path.realpath(__file__)[:-8] + filename, 'r', encoding='utf-8')
    csvfile = csv.reader(file)
    lists = []
    for item in csvfile:
        lists.append(item)
    return lists


def load(data_number=1):
    data = np.array(csv2list('mnist_train.csv'), dtype='int')
    X = data[:data_number, 1:]
    T = data[:data_number, :1]
    data_test = np.array(csv2list('mnist_test.csv'), dtype='int')
    x_test = data_test[:data_number, 0:]
    return X, T, x_test