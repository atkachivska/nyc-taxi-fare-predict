import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math
from sklearn.preprocessing import normalize
from xgboost import XGBRegressor


fold_path = "data/consolidated/"
def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_xgboost_model(train_file, c_val):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	xgb = XGBRegressor(n_estimators=100, learning_rate=0.50, gamma=0, subsample=0.75,
                           colsample_bytree=1, max_depth=5)
	model = xgb.fit(x_normal, y)

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


def run_xgboost(train_file, test_file, C):
	model = build_xgboost_model(train_file, C)
	(y_test, y_pred) = test_model(model, test_file)
	rmse = calculate_error(y_test, y_pred)
	return rmse

def run_n_fold_cross_validation(folds):
	
	c = 2**3
	total_rsme = 0
	for index in range(folds):
		print "fold = "+str(index)+" starting"
		train_file = fold_path+"train_file_"+str(index)+".txt"
		test_file = fold_path+"train_file_"+str(index)+".txt"
		rsme = run_xgboost(train_file, test_file, c)
		total_rsme = total_rsme + rsme
		print "rsme = "+rsme

	avg_rsme = total_rsme/10

	print "C = "+str(c)+" rsme = "+avg_rsme



if __name__== "__main__":
	# for i in range(1, 10):
		# run_n_fold_cross_validation(10)
	print run_xgboost("data/train_small.csv", "data/test_small.csv", 1)



