import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math
from sklearn.svm import SVR
from sklearn.preprocessing import normalize

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_svm_model(train_file, c_val):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x_normal = normalize(x, norm='l2')
	model = SVR(C=c_val, epsilon=0.2).fit(x_normal, y)

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


def run_sv_regression(train_file, test_file, C):
	model = build_svm_model(train_file, C)
	(y_test, y_pred) = test_model(model, test_file)
	rmse = calculate_error(y_test, y_pred)
	print rmse

if __name__== "__main__":
	for i in range(1, 10):
		run_sv_regression("data/train.csv", "data/test.csv", 2**i)



