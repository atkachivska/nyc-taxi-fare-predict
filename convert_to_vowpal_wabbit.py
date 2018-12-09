

def convert_to_vw(source_file, destination_file, is_test):
	source_file_pointer = open(source_file, "r")
	destination_file_pointer = open(destination_file, "w")
	index = 0
	while True:
		line = source_file_pointer.readline()

		if line == "":
			source_file_pointer.close()
			destination_file_pointer.close()
			break

		line_array = line.split(",")
		label = line_array[0]
		passengers = line_array[1]
		distance = line_array[2]
		is_weekend = line_array[3]
		start_time = line_array[4]
		pickup = line_array[5]
		drop_off = line_array[6]

		if is_test == False:
			dest_string = label + " | " + "passengers:"+passengers
		else:
			dest_string = "|"
		dest_string = dest_string + " "+"distance:"+distance
		dest_string = dest_string + " "+"is_weekend:"+is_weekend
		dest_string = dest_string + " "+"start_time:"+start_time
		dest_string = dest_string + " "+"pickup:"+pickup
		dest_string = dest_string + " "+"drop_off:"+drop_off

		destination_file_pointer.write(dest_string)

if __name__== "__main__":
	convert_to_vw("data/train_co_ord.csv", "data/master.vw", False)