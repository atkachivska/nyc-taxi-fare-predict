import numpy as np
import matplotlib.pyplot as plt
import pandas
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math
from sklearn.preprocessing import normalize
from create_data_files import create_data_file, create_train_test

fold_path = "data/consolidated/"
result_path = "results/offline"

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_linear_model(train_file):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	model = LinearRegression().fit(x_normal, y)

	return model


def test_model(model, test_file):
	data = load_data(test_file)
	x_test, y_test = split_into_xy(data)
	x_normal = normalize(x_test, norm='l2')
	y_pred = model.predict(x_normal)

	return (y_test, y_pred)

def calculate_error(y_test, y_pred):	
	mse =  mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)
	return rmse


def run_linear_regression(train_file, test_file):
	model = build_linear_model(train_file)
	(y_test, y_pred) = test_model(model, test_file)
	rmse = calculate_error(y_test, y_pred)
	return rmse

def run_n_fold_cross_validation(folds):
	
	total_rsme = 0
	for index in range(folds):
		print "fold = "+str(index)+" starting"
		train_file = fold_path+"train_file_"+str(index)+".txt"
		test_file = fold_path+"train_file_"+str(index)+".txt"
		rsme = run_linear_regression(train_file, test_file)
		total_rsme = total_rsme + rsme
		print "rsme = "+str(rsme)

	avg_rsme = total_rsme/10

	print " rsme = "+str(avg_rsme)


if __name__== "__main__":
	train_file = "data/train.csv"
	test_file = "data/test.csv"
	data_size = [10000, 50000, 100000, 200000, 500000, 1000000]
	for data in data_size:
		create_train_test(data, False)
		rmse = run_linear_regression(train_file, test_file)
		print rmse
		file_name = result_path + "squared_linear_"+str(data)+".csv"
		file_pointer = open(file_name, "w+")
		file_pointer.write(str(rmse))
		file_pointer.close()


