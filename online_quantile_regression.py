import statistics
import numpy as np
import os
import math

result_dir = "results/"
train_file = "train.vw"
test_file = "test.vw"
prediction_file = "prediction.vw"
model_file = "model.vw"
test_command_string = "vw -t -d test.vw -i model.vw -p prediction.vw --quiet"

def rmsle_func(y_pred, y) : 
    	assert len(y) == len(y_pred)
	terms_to_sum = [(math.log(y_pred[i] + 1) - math.log(y[i] + 1)) ** 2.0 for i,pred in enumerate(y_pred)]
	return (sum(terms_to_sum) * (1.0/len(y))) ** 0.5

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

	rmsle = rmsle_func(y_pred, y_test)
	print rmsle
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


if __name__ == '__main__':
	quantile_nn_train_command_string = "vw --nn 10 -d "+train_file+" --loss_function quantile --passes 10 --cache_file cache.ca --quantile_tau {0} -f "+model_file+" --quiet"
	quantile_train_command_string = "vw -d "+train_file+" --loss_function quantile --passes 10 --cache_file cache.ca --quantile_tau {0} -f "+model_file+" --quiet"
	squared_command_string = "vw -d "+train_file+" --loss_function squared --passes 10 --cache_file cache.ca -f "+model_file+" --quiet"
	squared_nn_command_string = "vw --nn 10 -d "+train_file+" --loss_function squared --passes 10 --cache_file cache.ca -f "+model_file+" --quiet"
	run_quantile_regression("results/quantile_results_nn.csv", quantile_nn_train_command_string)
	run_quantile_regression("results/quantile_results.csv", quantile_train_command_string)
	run_squared_regression("results/squared_results.csv", squared_command_string)
	run_squared_regression("results/squared_nn_results.csv", squared_nn_command_string)
	get_error_stats("any", 0.5)

