import matplotlib.pyplot as plt
from numpy import genfromtxt


#fare, number_of_passengers, distance, start_time_is_weekend, start_time_of_day,  pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude 

graph_path = "graphs/"
num_of_points = 10000

def load_data(filename):
	data = genfromtxt(filename, delimiter=',')
	return data


def split_into_xy(data):
	x, y = data[:, 1:], data[:, 0]
	return (x, y)

def plot_individual_feature(feature_x, y, feature):
	plt.scatter(feature_x, y)
	plt.title("plot")
	plt.xlabel(feature)
	plt.ylabel("Fare")
	plt.savefig(graph_path+"/"+feature+".png")
	plt.show()
	plt.close()


def plot_for_features(filename):
	data = load_data(filename)
	x, y = split_into_xy(data)
	x = x[:num_of_points]
	y = y[:num_of_points]
	num_passengers = []
	distance = []
	start_time_is_weekend = []
	start_time_of_day = []
	pickup_longitude = []
	pickup_latitude = []
	dropoff_longitude = []
	dropoff_latitude = []                                                                          #MOD 1:Input file format not clear, need to recheck with P.
	for each in x:
		num_passengers.append(each[0])	
		distance.append(each[1])
		start_time_is_weekend.append(each[2])
		start_time_of_day.append(each[3])
		pickup_longitude.append(each[4])
		pickup_latitude.append(each[5])
	plot_individual_feature(num_passengers, y, 'Number of Passengers')                                  #MOD 2: Make changes to labels accordingly
	plot_individual_feature(distance, y, 'Distance')
	plot_individual_feature(start_time_is_weekend, y, 'Is Weekend')
	plot_individual_feature(start_time_of_day, y, 'Time of Day')
	plot_individual_feature(pickup_longitude, y, 'Pickup')
	plot_individual_feature(pickup_latitude, y, 'DropoffJ')
	# plot_individual_feature(dropoff_longitude, y, 'dropoff_longitude')
	# plot_individual_feature(dropoff_latitude, y, 'dropoff_latitude')


if __name__== "__main__":
	print plot_for_features("data/master_data.csv")
