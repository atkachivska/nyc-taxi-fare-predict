import statistics
import numpy as np
import os

result_dir = "results/"
data_file = "master.vw"
prediction_file = "prediction.vw"

def temp_error_file(train_file, prediction_file):
	train_file_pointer = open(train_file, "r")
	prediction_file_pointer = open(prediction_file, "r")

	while True:
	train_line = train_file_pointer.readline()
	if train_line == "":
		train_file_pointer.close()
		prediction_file_pointer.close()
		break

	train_line_split = train_line.split("|")
	train_label = float(train_line_split[0].strip())
	prediction_value = prediction_file_pointer.readline().strip()
	prediction = float(prediction_value)
	error = abs(train_label - prediction)
	error_list.append(error)
	index = index + 1

	print len(error_list), quantile
	mean_error = statistics.mean(error_list)
	std_dev_error = statistics.stdev(error_list)


def get_error_stats(train_file, prediction_file, result_file_pointer, quantile):
	train_file_pointer = open(train_file, "r")
	prediction_file_pointer = open(prediction_file, "r")

	error_list = []
	index = 0
	while True:
		train_line = train_file_pointer.readline()
		if train_line == "":
			train_file_pointer.close()
			prediction_file_pointer.close()
			break

		train_line_split = train_line.split("|")
		train_label = float(train_line_split[0].strip())
		prediction_value = prediction_file_pointer.readline().strip()
		prediction = float(prediction_value)
		error = abs(train_label - prediction)
		error_list.append(error)
		index = index + 1

	print len(error_list), quantile
	mean_error = statistics.mean(error_list)
	std_dev_error = statistics.stdev(error_list)
	print mean_error
	print std_dev_error
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
	command = command_string.format(data_file, prediction_file)
	os.system(command)
	get_error_stats(data_file, prediction_file, result_file_pointer, None)

def run_quantile_regression(result_file, command_string):
	result_file_pointer = open(result_file, "w")
	os.chdir(os.getcwd()+"/data")
	for quantile in np.arange(0.1, 1, 0.1):
		command = command_string.format(data_file, quantile, prediction_file)
		print command
		# print os.system("pwd")
		os.system(command)
		get_error_stats(data_file, prediction_file, result_file_pointer, quantile)


if __name__ == '__main__':
	quantile_command_string = "vw -d {0} --loss_function quantile --quantile_tau {1} --passes 1 -p {2} --quiet"
	quantile_nn_command_string = "vw -d {0} --loss_function quantile --quantile_tau {1} --passes 1 -p {2} --quiet --nn 10"
	squared_command_string = "vw -d {0} --loss_function squared --passes 1 -p {1} --quiet"
	squared_nn_command_string = "vw -d {0} --loss_function squared --passes 1 -p {1} --quiet --nn 10"
	# run_quantile_regression("results/quantile_results.csv", quantile_command_string)
	# run_quantile_regression("results/quantile_results_nn.csv", quantile_nn_command_string)
	# run_squared_regression("results/squared_results.csv", squared_command_string)
	run_squared_regression("results/squared_nn_results.csv", squared_nn_command_string)

