import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas
from sklearn.cluster import KMeans
from numpy import genfromtxt
from sklearn.linear_model import LinearRegression

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)


def run_linear_regression(filename):
	data = load_data(filename)
	x, y = split_into_xy(data)
	reg = LinearRegression().fit(x, y)
	print reg.coef_


if __name__== "__main__":
	run_linear_regression("train_co_ord.csv")