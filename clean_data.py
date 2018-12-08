
import time
from datetime import datetime
from haversine import haversine
date_pattern = '%Y-%m-%d %H:%M:%S'
#date format : 2012-05-12 05:09:05.0000002
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


def get_number_of_lines(filename):
	file_pointer = open(filename, "r")
	index = 0
	while True:
		line = file_pointer.readline()
		if line == "":
			break
		index = index + 1
		if index % 10000000 == 0:
			print line

	print index

def clean_date_string(date_string):
	return date_string[:19]


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

def process_for_dates(source_file, destination_file):
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
  process_for_dates("train.csv", "train_dates_done.csv")





