from online_quantile_regression import get_result_file
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
analytics_folder = "analytics/"

algo_type_list = ['linear', 'nn']
loss_function_list = ['squared', 'quantile']
data_size_list = [10000, 50000, 100000, 200000, 500000, 1000000]



def quantiles_for_million_data_set():
	file_name = analytics_folder+"linear_quartiles.csv"
	file_pointer = open(file_name, "w+")
	results_file = get_result_file("linear", "quantile", 1000000)
	results_file_pointer = open(results_file, "r+")

	file_pointer.write("Percentile,RMSE, STD DEV,"+ ",".join(str(round(quantile, 2)) for quantile in np.arange(0.1, 1.1, 0.1)) + '\n')
	rmse_array = ["rsme"]
	for line in results_file_pointer.readlines():
		data_array = line.split(",")
		result_array = []
		result_array.append(round(float(data_array[0]), 2))
		result_array.append(round(float(data_array[1]), 2))
		result_array.append(round(float(data_array[2]), 2))
		for index in range(4, 24, 2):
			result_array.append(round(float(data_array[index]), 2))

		file_pointer.write(','.join(str(val) for val in result_array) + '\n')

	file_pointer.close()
	results_file_pointer.close()




def process_rmse():
	file_name = analytics_folder+"rmse.csv"

	file_pointer = open(file_name, "w+")
	data_str = "Type," + ','.join(str(node) for node in data_size_list) + '\n'
	file_pointer.write(data_str)

	file_pointer.write("Linear Squared," + ','.join(str(node) for node in get_rmse_error_list('linear', 'squared')) + '\n')
	file_pointer.write("NN Squared," + ','.join(str(node) for node in get_rmse_error_list('nn', 'squared')) + '\n')
	file_pointer.write("Linear Quantile," + ','.join(str(node) for node in get_rmse_error_list('linear', 'quantile')) + '\n')
	file_pointer.write("NN Quantile," + ','.join(str(node) for node in get_rmse_error_list('nn', 'quantile')) + '\n')

	file_pointer.close()


def get_rmse_error_list(algo_type, loss_function):

	ret_array = []
	for data in data_size_list:
		if loss_function == 'squared':
			ret_array.append(get_squared_rmse_error(data, algo_type))
		else:
			ret_array.append(get_quantile_rmse_error(data, algo_type))

	return ret_array




def get_quantile_rmse_error(data_size, algo_type):
	file_name = get_result_file(algo_type, "quantile", data_size)
	file_pointer = open(file_name, "r")

	min_rmse = 10000
	for line in file_pointer.readlines():
		rmse_array = line.split(",")
		min_rmse = min(min_rmse, round(float(rmse_array[1]), 2))

	file_pointer.close()
	return min_rmse


def get_squared_rmse_error(data_size, algo_type):
	file_name = get_result_file(algo_type, "squared", data_size)
	file_pointer = open(file_name, "r")
	rmse_str = file_pointer.readline()
	rmse_array = rmse_str.split(",")
	file_pointer.close()
	rmse_error = round(float(rmse_array[0]), 2)
	return rmse_error



if __name__ == '__main__':
	quantiles_for_million_data_set()
	# process_rmse()
