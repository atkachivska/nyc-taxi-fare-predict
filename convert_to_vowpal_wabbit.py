

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
			dest_string = label + " | " + "0:"+passengers
		else:
			dest_string = "|"
		dest_string = dest_string + " "+"1:"+distance
		dest_string = dest_string + " "+"2:"+is_weekend
		dest_string = dest_string + " "+"3:"+start_time
		dest_string = dest_string + " "+"4:"+pickup
		dest_string = dest_string + " "+"5:"+drop_off

		destination_file_pointer.write(dest_string)

if __name__== "__main__":
	convert_to_vw("data/train.csv", "data/train.vw", False)
	convert_to_vw("data/test.csv", "data/test.vw", True)