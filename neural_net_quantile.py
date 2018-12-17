import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation
import keras.backend as K
from sklearn.preprocessing import normalize
from sklearn.metrics import mean_squared_error
import math
import tensorflow as tf
from create_data_files import create_train_test
import statistics
from utils import get_error_stats, split_into_xy, train_file, test_file, offline_result_path, write_header_names, batch_data_size_array

quant = [0.5]
#np.arange(0.1, 1, 0.1)
# data_size = [100, 500, 1000, 5000, 10000, 50000, 100000]
# data_size = [10, 100, 500]   # for testing
result_file = offline_result_path+'neural_network_quantile.csv'


def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def define_model():
    model = Sequential()
    model.add(Dense(units=10, input_dim=6,activation='relu'))
    model.add(Dense(units=10, input_dim=6,activation='relu'))
    model.add(Dense(1))
    return model

def tilted_loss(q,y,f):
    e = (y-f)
    return K.mean(K.maximum(q*e, (q-1)*e), axis=-1)

def test_model(model, test_file):
	data = load_data(test_file)
	y_pred = []
	x_test, y_test = split_into_xy(data)
	x_normal = normalize(x_test, norm='l1')
	y_temp = model.predict(x_normal)
	for temp in y_temp:
		y_pred.append(temp[0])
	return (y_test, y_pred)

def build_models_on_quantile(train_file):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l1')
	model = define_model()
	model.compile(loss=lambda y, f: tilted_loss(0.5,y,f), optimizer='adadelta')
	model.fit(x_normal, y, epochs=50, batch_size=34, verbose=0)
	return model 

def run_neural_net_quantile_regression():
	result_file_pointer = open(result_file, 'w+')
	write_header_names(result_file_pointer)
	for size in batch_data_size_array:
		create_train_test(size, False)
		model = build_models_on_quantile(train_file)
		(y_test, y_pred) = test_model(model, test_file)
		get_error_stats(y_test, y_pred, result_file_pointer, size)
	result_file_pointer.close()

if __name__== "__main__":
	run_neural_net_quantile_regression()