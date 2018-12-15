
import time
from datetime import datetime
from haversine import haversine
date_pattern = '%Y-%m-%d %H:%M:%S'
#date format : 2012-05-12 05:09:05
def convert_date_to_epoch(date_string):
	if len(date_string) > 19:
		raise Exception("Date String not in right format") 

	epoch = int(time.mktime(time.strptime(date_string, date_pattern)))
	return epoch

def get_time_of_day_from_epoch(epoch):
	return epoch % (24 * 60 * 60)

def get_is_date_string_weekend(date_string):
	datetime_object = datetime.strptime(date_string, date_pattern)
	if datetime_object.weekday() < 5:
		return 0
	else:
		return 1

#takes the source file which is the train file from kaggle 
#and a destination file pointer and moves upto 1M data points to the file
def create_master_file(source_file, destination_file):
	source_file_pointer = open(source_file, "r")
	destination_file_pointer = open(destination_file, "w+")

	index = 0
	while True:
		line = source_file_pointer.readline()
		if line == "" or index == 1000000:
			break

		destination_file_pointer.write(line)
		index = index + 1

#takes string of format 2009-06-15 17:26:21 UTC
#and returns string of format 2009-06-15 17:26:21
def clean_date_string(date_string):
	return date_string[:19]


#for each data point in the file,
#converts date into time of day epoch
#adds is_weekend feature
#adds haversine distance between two co ordinates
#returns all features in array format
def process_entry(file_string):
	string_array = file_string.split(",")

	start_date_string = clean_date_string(string_array[2])
	start_time_epoch = convert_date_to_epoch(start_date_string)
	start_time_of_day = get_time_of_day_from_epoch(start_time_epoch)
	start_time_is_weekend = get_is_date_string_weekend(start_date_string)

	fare = float(string_array[1])
	if fare <= 0:
		return None
	pickup_longitude = float(string_array[3])
	pickup_latitude = float(string_array[4])

	dropoff_longitude = float(string_array[5])
	dropoff_latitude = float(string_array[6])
	number_of_passengers = int(string_array[7])

	distance = round(haversine((pickup_latitude, pickup_longitude), (dropoff_latitude, dropoff_longitude)), 2)

	new_array = [fare, number_of_passengers, distance, start_time_is_weekend, start_time_of_day,  pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude ]
	return new_array

#converts data into standard format from soruce file and puts it into destination file
def clean_data(source_file, destination_file):
	source_pointer = open(source_file, "r")
	dest_pointer = open(destination_file, "w")
	index = 0
	while True:
		try:
			source_line = source_pointer.readline()

			if source_line == "" or index > 1000000:
				source_pointer.close()
				dest_pointer.close()
				break

			dest_format_array = process_entry(source_line)
			if dest_format_array == None:
				continue
			#create a string out of array
			dest_format_string = ','.join(str(node) for node in dest_format_array) + '\n'
			dest_pointer.write(dest_format_string)

			index = index + 1
		except ValueError as e:
			print e
			print "Error parsing file with index = "+str(index)

	


if __name__== "__main__":
	create_master_file("../vault/train.csv", "data/master_before_changes.csv")
  	# clean_data("data/master_before_changes.csv", "data/master_before_knn.csv")





