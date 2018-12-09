import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas
from sklearn.cluster import KMeans
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math
from sklearn.preprocessing import normalize
from sklearn.linear_model import Ridge

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def build_ridge_model(train_file, alpha):
	data = load_data(train_file)
	x, y = split_into_xy(data)
	x = normalize(x, norm='l2')
	model = Ridge(alpha=alpha).fit(x, y)

	return model


def test_model(model, test_file):
	data = load_data(test_file)
	x_test, y_test = split_into_xy(data)
	x = normalize(x_test, norm='l2')
	y_pred = model.predict(x)

	return (y_test, y_pred)

def calculate_error(y_test, y_pred):	
	mse =  mean_squared_error(y_test, y_pred)
	rmse = math.sqrt(mse)
	return rmse


def run_ridge_regression(train_file, test_file, alpha):
	model = build_ridge_model(train_file, alpha)
	(y_test, y_pred) = test_model(model, test_file)
	rmse = calculate_error(y_test, y_pred)
	print rmse

if __name__== "__main__":
	for i in range(-5, 5):
		run_ridge_regression("data/train.csv", "data/test.csv", 2**i)