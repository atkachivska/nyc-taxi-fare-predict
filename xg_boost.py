import numpy as np
from numpy import genfromtxt
from sklearn.preprocessing import normalize
from xgboost import XGBRegressor
from create_data_files import create_data_file, create_train_test
from utils import offline_result_path, split_into_xy, load_data, batch_data_size_array, write_header_names, train_file, test_file, get_error_stats
fold_path = "data/consolidated/"
result_file = offline_result_path+'xgboost.csv'

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_xgboost_model(train_file, max_depth):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	
	xgb = XGBRegressor(n_estimators=100, learning_rate=0.20,subsample=0.75,  max_depth=max_depth)
	model = xgb.fit(x_normal, y)

	return model


def test_model(model, test_file):
	data = load_data(test_file)
	x_test, y_test = split_into_xy(data)
	x_normal = normalize(x_test, norm='l2')
	y_pred = model.predict(x_normal)

	return (y_test, y_pred)

def run_xg_boost():
	result_file_pointer = open(result_file, 'w+')
	write_header_names(result_file_pointer)
	for size in batch_data_size_array:
		create_train_test(size, False)
		model = build_xgboost_model(train_file, 8)
		(y_test, y_pred) = test_model(model, test_file)
		get_error_stats(y_test, y_pred, result_file_pointer, size)
	result_file_pointer.close()



def run_xgboost_for_validation(train_file, test_file, max_depth):
	model = build_xgboost_model(train_file, max_depth)
	(y_test, y_pred) = test_model(model, test_file)
	rmse = math.sqrt(mean_squared_error(y_test, y_pred))
	rmsle = rmsle_func(y_pred, y_test)
	error_list = []
	for index in range(len(y_test)):
		error_list.append(abs(y_test[index]- y_pred[index]))

	std_dev_error = statistics.stdev(error_list)
	return [rmse, rmsle, std_dev_error]

def run_n_fold_cross_validation(folds, max_depth):
	
	total_rmse = 0
	total_rmsle = 0
	total_stddev = 0
	for index in range(folds):
		print "fold = "+str(index)+" starting"
		train_file = fold_path+"train_file_"+str(index)+".txt"
		test_file = fold_path+"train_file_"+str(index)+".txt"
		stat_tuple = run_xgboost_for_validation(train_file, test_file, max_depth)
		total_rmse = total_rmse + stat_tuple[0]
		total_rmsle = total_rmsle + stat_tuple[1]
		total_stddev = total_stddev + stat_tuple[2]

	avg_rmse = total_rmse/folds
	avg_rmsle = total_rmsle/folds
	avg_stddev = total_stddev/folds

	result_array = []
	result_array.append(max_depth)
	result_array.append(avg_rmse)
	result_array.append(avg_rmsle)
	result_array.append(avg_stddev)
	result_string = ",".join(str(node) for node in result_array) + "\n"
	print result_array

def run_validation():
	for index in range(7, 9, 1):
		run_n_fold_cross_validation(10, index)

if __name__== "__main__":
	run_xg_boost()


