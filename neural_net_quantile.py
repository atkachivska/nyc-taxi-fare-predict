import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation
from numpy import genfromtxt
import keras.backend as K
from sklearn.preprocessing import normalize
from sklearn.metrics import mean_squared_error
import math
import tensorflow as tf
from create_data_files import create_train_test
import statistics

quant = [0.5]
#np.arange(0.1, 1, 0.1)
data_size = [100, 500, 1000, 5000, 10000, 50000, 100000]   # for testing
result_file = 'results/offline/quantile_neural/error.csv'

def rmsle_func(y_pred, y) :
	try: 
		terms_to_sum = [(math.log(y_pred[i] + 1) - math.log(y[i] + 1)) ** 2.0 for i,pred in enumerate(y_pred)]
	except ValueError as e:
		print(e.detail)
	return (sum(terms_to_sum) * (1.0/len(y))) ** 0.5

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

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
	x_normal = normalize(x_test, norm='l2')
	y_temp = model.predict(x_normal)
	for temp in y_temp:
		y_pred.append(temp[0])
	return (y_test, y_pred)

def build_models_on_quantile(train_file):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	models = [{}]
	for qt in quant:
		model = define_model()
		model.compile(loss=lambda y, f: tilted_loss(qt,y,f), optimizer='adadelta')
		model.fit(x_normal, y, epochs=50, batch_size=34, verbose=0)   
		models.append({'qt':qt, 'model':model})
	models.pop(0)
	return models

def get_error_stats(y_test, y_pred, result_file_pointer, quantile):
	error_list = []
	index = 0
	while index<len(y_test):
		error = abs(y_test[index] - y_pred[index])
		error_list.append(error)
		index = index + 1
	rmsle = rmsle_func(y_pred, y_test)
	mean_error = statistics.mean(error_list)
	std_dev_error = statistics.stdev(error_list)
	percentile_errors = []
	for i in range(0, 100, 5):
		percentile_errors.append(np.percentile(error_list, i))
	result_array = []
	if quantile != None:
		result_array.append(quantile)
	result_array.append(mean_error)
	result_array.append(std_dev_error)
	result_array.extend(percentile_errors)
	result_string = ",".join(str(node) for node in result_array)
	result_string = result_string+"\n"
	result_file_pointer.write(result_string)

def run_neural_net_quantile_regression(train_file, test_file):
	result_file_pointer = open(result_file, 'w')
	models = build_models_on_quantile(train_file)
	for element in models:
		(y_test, y_pred) = test_model(element['model'], test_file)
		get_error_stats(y_test, y_pred, result_file_pointer, element['qt'])

if __name__== "__main__":
	#create_train_test(data_size, False)
	run_neural_net_quantile_regression("data/train.csv", "data/test.csv")