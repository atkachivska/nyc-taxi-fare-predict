import numpy as np
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import pandas
from sklearn.cluster import KMeans
from numpy import genfromtxt


def load_data(filename):
	colnames = ['latitude', 'longitude']
	data = pandas.read_csv(filename, names=colnames)
	return data


def load_file(filename):
	data = genfromtxt(filename, delimiter=',')
	return data

def splice_co_ordinates(ndarray):
	pickup_co_ordinates = ndarray[:, [5,6]]
	dropoff_co_ordinates = ndarray[:, [7,8]]

	return np.concatenate((pickup_co_ordinates, dropoff_co_ordinates), axis=0)

def splice_time_of_day(ndarray):
	time_of_day = ndarray[:, [4]]
	return time_of_day

def build_model_for_time_of_day(clusters, data):
	kmeans = KMeans(n_clusters=clusters)
	model = kmeans.fit(data)
	return model


def build_model_for_co_ordinates(clusters, data):
	kmeans = KMeans(n_clusters=clusters)
	model = kmeans.fit(data)
	return model

def find_elbow(filename):
	ndarray = load_file(filename)
	data = splice_co_ordinates(ndarray)
	K = range(2,50)
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
	ax.plot(K[kIdx], avgWithinSS[kIdx])
	plt.grid(True)
	plt.xlabel('Number of clusters')
	plt.ylabel('Average within-cluster sum of squares')
	tt = plt.title('Elbow for K-Means clustering of co ordinates')
	plt.show() 

def write_back_to_file(source_file,  destination_file, co_ordinate_model, time_of_day_model):
	source_file_pointer = open(source_file, "r")
	destination_file_pointer = open(destination_file, "w")
	while True:
		temp_string = source_file_pointer.readline()
		if temp_string == "":
			source_file_pointer.close()
			destination_file_pointer.close()
			break

		string_list = temp_string.split(",")
		pickup_co_ordinates = [string_list[5], string_list[6]]
		dropoff_co_ordinates = [string_list[7], string_list[8]]
		time_of_day = [string_list[4]]

		pickup_cluster = co_ordinate_model.predict(pickup_co_ordinates)
		dropoff_cluster = co_ordinate_model.predict(dropoff_co_ordinates)
		time_of_day_cluster = time_of_day_model.predict(time_of_day)

		string_list = string_list[:4]
		
		
		string_list.append(time_of_day_cluster.tolist()[0])
		string_list.append(pickup_cluster.tolist()[0])
		string_list.append(dropoff_cluster.tolist()[0])



		dest_string = ','.join(str(node) for node in string_list) + '\n'
		destination_file_pointer.write(dest_string)




def run_knn(model_file, source_file, destination_file, co_ordinate_clusters, time_of_day_clusters):
	ndarray = load_file(model_file)
	co_ordinate_data = splice_co_ordinates(ndarray)
	co_ordinate_model = build_model_for_co_ordinates(co_ordinate_clusters, co_ordinate_data)
	time_of_day_data = splice_time_of_day(ndarray)
	time_of_day_model = build_model_for_time_of_day(time_of_day_clusters, time_of_day_data)
	write_back_to_file(source_file, destination_file, co_ordinate_model, time_of_day_model)


if __name__== "__main__":
	# find_elbow("data/knn_source.csv")
	run_knn("data/knn_source.csv", "data/master_before_knn.csv", "data/master_data.csv",  30, 20)



