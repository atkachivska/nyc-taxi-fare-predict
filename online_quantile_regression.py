import statistics
import numpy as np
import os
import math
from create_data_files import create_train_test

test_file = "test.vw"
prediction_file = "prediction.vw"
model_file = "model.vw"
test_command_string = "vw -t -d test.vw -i model.vw -p prediction.vw"
train_command_string = "vw -d train.vw --loss_function {0} --passes 10 --cache_file cache.ca -f model.vw"

def get_error_stats(result_file_pointer, quantile):
	test_file_pointer = open(test_file, "r")
	prediction_file_pointer = open(prediction_file, "r")

	error_list = []
	y_pred = []
	y_test = []
	index = 0
	while True:
		test_line = test_file_pointer.readline()
		if test_line == "":
			test_file_pointer.close()
			prediction_file_pointer.close()
			break

		test_line_split = test_line.split("|")
		test_label = float(test_line_split[0].strip())
		prediction_value = prediction_file_pointer.readline().strip()
		prediction = float(prediction_value)
		error = abs(test_label - prediction)
		y_pred.append(prediction)
		y_test.append(test_label)
		error_list.append(error)
		index = index + 1

	mean_error = statistics.mean(error_list)
	std_dev_error = statistics.stdev(error_list)
	print quantile, mean_error, std_dev_error
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

def run_squared_regression(result_file, command_string):
	result_file_pointer = open(result_file, "w+")
	os.chdir(os.getcwd()+"/data")
	print command_string
	os.system(command_string) #train
	os.system(test_command_string)
	get_error_stats(result_file_pointer, None)

def run_quantile_regression(result_file, command_string):
	create_train_test(data_size)
	result_file_pointer = open(result_file, "w")
	os.chdir(os.getcwd()+"/data")
	for quantile in np.arange(0.1, 1, 0.1):
		command = command_string.format(quantile)
		print command
		os.system(command)
		os.system(test_command_string)
		get_error_stats(result_file_pointer, quantile)
		os.system("rm "+prediction_file)
		os.system("rm "+model_file)

def clean_up():
	os.remove("cache.ca")
	os.remove(model_file)
	os.remove(prediction_file)

def run_algorithm(algo_type, loss_function, data_size):

	train_command = train_command_string.format(loss_function)
	if algo_type == 'nn':
		train_command = train_command + " --nn 10 "

	result_file = get_result_file(algo_type, loss_function, data_size)
	result_file_pointer = open(result_file, "w")
	os.chdir("./data")
	if loss_function == 'quantile':
		for quantile in np.arange(0.1, 1, 0.1):
			print os.path.abspath(os.curdir)
			quantile_train_command = train_command + " --quantile_tau "+str(quantile)
			print quantile_train_command
			print test_command_string
			os.system(quantile_train_command)
			os.system(test_command_string)
			get_error_stats(result_file_pointer, quantile)
			clean_up()
	else:
		os.system(train_command)
		os.system(test_command_string)
		get_error_stats(result_file_pointer, None)
		clean_up()

	os.chdir("..")


def get_result_file(algo_type, loss_function, data_size):
	return "results/"+loss_function+"_"+algo_type+"_"+str(data_size)+"_results.csv"



def create_run_sequence():
	algo_type_list = ['linear', 'nn']
	loss_function_list = ['squared', 'quantile']
	data_size_list = [10000, 50000, 100000, 200000, 500000, 1000000]
	for data_size in data_size_list:
		create_train_test(data_size, True)
		for algo_type in algo_type_list:
			for loss_function in loss_function_list:
				run_algorithm(algo_type, loss_function, data_size)


if __name__ == '__main__':
	create_run_sequence()