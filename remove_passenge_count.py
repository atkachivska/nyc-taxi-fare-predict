
def drop_passenger_count(source_filename, destination_filename):
	source_file_pointer = open(source_filename, "r")
	destination_file_pointer = open(destination_filename, "w")

	while True:
		line = source_file_pointer.readline()
		if line == "":
			source_file_pointer.close()
			destination_file_pointer.close()
			break

		line_array = line.split(",")
		del line_array[1]
		string = ",".join(line_array)
		destination_file_pointer.write(string)


if __name__== "__main__":
	drop_passenger_count( "data/master.csv", "data/master_no_passengers.csv")