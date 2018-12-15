import numpy as np
import matplotlib.pyplot as plt
import pandas
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math
from sklearn.preprocessing import normalize
from create_data_files import create_data_file, create_train_test
from utils import split_into_xy, get_error_stats, train_file, test_file, offline_result_path, batch_data_size_array, offline_result_path, write_header_names


def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data


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


def run_linear_regression():
	result_file_name = offline_result_path+'linear_regression.csv'
	result_file_pointer = open(result_file_name, "w+")
	write_header_names(result_file_pointer)
	for size in batch_data_size_array:
		create_train_test(size, False)
		model = build_linear_model(train_file)
		(y_test, y_pred) = test_model(model, test_file)
		get_error_stats(y_test, y_pred, result_file_pointer, size)
	result_file_pointer.close()


if __name__== "__main__":
	run_linear_regression()

