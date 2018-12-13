import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from numpy import genfromtxt
from statsmodels.regression.quantile_regression import QuantReg
from sklearn.metrics import mean_squared_error
import math
from sklearn.preprocessing import normalize
import statsmodels.formula.api as smf
import pandas as pd

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_quantile_model(train_file):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	final = {'x':np.array(x_normal), 'y':np.array(y)}
	mod = smf.quantreg('y ~ x', final)
	return mod


def matmult(a,b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]


def test_model(mod, test_file):
	data = load_data(test_file)
	x_test, y_test = split_into_xy(data)
	x_normal = normalize(x_test, norm='l2')
	y_pred = []
	y_pred = mod.params['Intercept'] +  matmult([[mod.params['x[0]']], [mod.params['x[1]']], [mod.params['x[2]']], [mod.params['x[3]']], [mod.params['x[4]']], [mod.params['x[5]']]], x_normal)
	return (y_test, y_pred)


def rmsle_func(y_pred, y) : 
	terms_to_sum = [(math.log(y_pred[i] + 1) - math.log(y[i] + 1)) ** 2.0 for i,pred in enumerate(y_pred)]
	return (sum(terms_to_sum) * (1.0/len(y))) ** 0.5


def get_error_stats(y_test, y_pred, qtile):
	error_list = []
	index = 0
	i=0
	while i<len(y_test):
		error = abs(y_test[i] - y_pred[i])
		error_list.append(error)
		index = index + 1
	rmsle = rmsle_func(y_pred, y_test)
	print rmsle
	mean_error = statistics.mean(error_list)
	std_dev_error = statistics.stdev(error_list)
	print qtile, mean_error, std_dev_error
	percentile_errors = []
	for i in range(0, 100, 5):
		percentile_errors.append(np.percentile(error_list, i))

	result_array = []
	if qtile != None:
		result_array.append(qtile)
	result_array.append(mean_error)
	result_array.append(std_dev_error)
	result_array.extend(percentile_errors)

	result_string = ",".join(str(node) for node in result_array)
	result_string = result_string+"\n"

	result_file_pointer = open('/results/qtile_regression_offline.csv', 'a')
	result_file_pointer.write(result_string)


def run_quantile_regression(train_file, test_file):
	quantiles = np.arange(0.1,1,0.1)
	models = []
	params = []
	mod = build_quantile_model(train_file)

	for qt in quantiles:
		res = mod.fit(q = qt)
		print(res.summary())
		models.append(res)
		lower_b = []
		upper_b = []
		for each in ['x[0]', 'x[1]', 'x[2]', 'x[3]', 'x[4]', 'x[5]']:
			li = res.conf_int().ix[each].tolist()
			lower_b.append(li[0])
			upper_b.append(li[1])
		
		params.append(
			[qt, 
			res.params['Intercept'], 
			[res.params['x[0]'], res.params['x[1]'], res.params['x[2]'], res.params['x[3]'], res.params['x[4]'], res.params['x[5]']], 
			upper_b,
			lower_b])
		# (y_test, y_pred) = test_model(res, test_file)             #TODO: Check for multi features!!
		# get_error_stats(y_test, y_pred, qt)

	params = pd.DataFrame(data = params, columns = ['qt','intercept','x_coef','cf_lower_bound','cf_upper_bound'])
	print(params)



if __name__== "__main__":
	run_quantile_regression("data/train.csv", "data/test.csv")