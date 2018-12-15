from sklearn.metrics import mean_squared_error
from math import sqrt
from numpy import genfromtxt
import statistics
import math
import numpy as np

train_file = "data/train.csv"
test_file = "data/test.csv"
offline_result_path = "results/offline/"
online_result_path = "results/online/"
batch_data_size_array = [100, 500, 1000, 5000, 10000, 50000, 100000]


def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def write_header_names(file_pointer):
	string = "Data Size, Mean Error, RMSE, RMSLE, STD_DEV"
	for percentile in range(0, 100, 10):
		string = string + ","+str(percentile)

	string = string + "\n"
	file_pointer.write(string)


def rmsle_func(real, predicted):
    sum=0.0
    for x in range(len(predicted)):
        if predicted[x]<0 or real[x]<0: #check for negative values
            continue
        p = np.log(predicted[x]+1)
        r = np.log(real[x]+1)
        sum = sum + (p - r)**2
    return (sum/len(predicted))**0.5

#takes the list of predicted and tested values, calculates stats and prints the data into file pointer provided
def get_error_stats(y_test, y_pred, result_file_pointer, data_size, quantile=0):
	error_list = []
	index = 0
	while index<len(y_test):
		error = abs(y_test[index] - y_pred[index])
		error_list.append(error)
		index = index + 1

	rmsle = rmsle_func(y_pred, y_test)
	mean_error = statistics.mean(error_list)
	rmse = sqrt(mean_squared_error(y_test, y_pred))
	std_dev_error = statistics.stdev(error_list)
	percentile_errors = []
	for i in range(0, 100, 10):
		percentile_errors.append(round(np.percentile(error_list, i), 2))
	result_array = []
	result_array.append(round(data_size, 2))
	result_array.append(round(mean_error, 2))
	result_array.append(round(rmse, 2))
	result_array.append(round(rmsle, 2))
	result_array.append(round(std_dev_error, 2))
	result_array.extend(percentile_errors)
	result_string = ",".join(str(value) for value in result_array)
	result_string = result_string+"\n"
	result_file_pointer.write(result_string)