import matplotlib.pyplot as plt
from numpy import genfromtxt


# FEATURE: passengers, distance, is_weekend, start_time, pickup, drop off

graph_path = "graphs/"
num_of_points = 10000
distance_threshold = 100

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data


def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)



def plot_individual_feature(feature_x, y, feature):
	print feature
	plt.scatter(feature_x, y)
	plt.title("plot")
	plt.xlabel(feature)
	plt.ylabel("Fare")
	plt.savefig(graph_path+"/"+feature+".png")
	plt.show()
	plt.close()


def plot_for_features(filename):
	data = load_data(filename)
	x, y_temp = split_into_xy(data)
	x = x[:num_of_points]
	y_temp = y_temp[:num_of_points]
	num_passengers = []
	y_num_passengers = []
	distance = []
	y_distance = []
	start_time_is_weekend = []
	y_start_time_is_weekend = []
	start_time_of_day = []
	y_start_time_of_day = []
	pickup_longitude = []
	y_pickup_longitude = []
	pickup_latitude = []
	y_pickup_latitude = []
	i=0
	while i<len(x):
		num_passengers.append(x[i][0])	
		y_num_passengers.append(y_temp[i])
		if x[i][1] < distance_threshold:
			distance.append(x[i][1])
			y_distance.append(y_temp[i])
		start_time_is_weekend.append(x[i][2])
		y_start_time_is_weekend.append(y_temp[i])
		start_time_of_day.append(x[i][3])
		y_start_time_of_day.append(y_temp[i])
		pickup_longitude.append(x[i][4])
		y_pickup_longitude.append(y_temp[i])
		pickup_latitude.append(x[i][5])
		y_pickup_latitude.append(y_temp[i])
		i = i+1
	plot_individual_feature(num_passengers, y_num_passengers, 'Number of Passengers')
	plot_individual_feature(distance, y_distance, 'Distance')
	plot_individual_feature(start_time_is_weekend, y_start_time_is_weekend, 'Is Weekend')
	plot_individual_feature(start_time_of_day, y_start_time_of_day, 'Time of Day')
	plot_individual_feature(pickup_longitude, y_pickup_longitude, 'Pickup')
	plot_individual_feature(pickup_latitude, y_pickup_latitude, 'Dropoff')


if __name__== "__main__":
	plot_for_features("data/master_data.csv")
