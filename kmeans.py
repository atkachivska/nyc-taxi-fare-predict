import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas
from sklearn.cluster import KMeans


def load_data(filename):
	colnames = ['latitude', 'longitude']
	data = pandas.read_csv(filename, names=colnames)
	return data

def create_model(clusters, data):
	kmeans = KMeans(n_clusters=clusters)
	model = kmeans.fit(data)
	return model

def cluster_points(model, data)
	labels = model.predict(data)
	return labels

def find_elbow(filename):
	data = load_data(filename).values

	K = range(1,10)
	KM = [kmeans(data,k) for k in K]
	centroids = [cent for (cent,var) in KM]
	D_k = [cdist(data, cent, 'euclidean') for cent in centroids]
	cIdx = [np.argmin(D,axis=1) for D in D_k]
	dist = [np.min(D,axis=1) for D in D_k]
	avgWithinSS = [sum(d)/data.shape[0] for d in dist]
	kIdx = 2
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(K, avgWithinSS, 'b*-')
	ax.plot(K[kIdx], avgWithinSS[kIdx], marker='o', markersize=12, 
      markeredgewidth=2, markeredgecolor='r', markerfacecolor='None')
	plt.grid(True)
	plt.xlabel('Number of clusters')
	plt.ylabel('Average within-cluster sum of squares')
	tt = plt.title('Elbow for K-Means clustering')
	plt.show() 

def return_data(filename, clusters):
	data = load_data(filename).values
	
	fp = open(filename)
	clustered_data = cluster_points(clusters, data)
	ret_array = []
	index = 0
	clustered_list = clustered_data.tolist()
	for line in fp.readlines():
		lat_long = line.split(",")
		temp = []
		for data in lat_long:
			temp.append(data.strip())
		temp.append(clustered_list[index])
		index = index + 1
		ret_array.append(temp)

	print ret_array

def main():
	return_data("/Users/praveenoak/Downloads/pre_run.csv", 10)
	# find_elbow("/Users/praveenoak/Downloads/pre_run.csv")


if __name__== "__main__":
  main()