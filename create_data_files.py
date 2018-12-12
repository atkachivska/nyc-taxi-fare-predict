master_data_file = "data/master_data.csv"
temp_data_file = "data/temp_data.csv"
def split_data(source_file, dest_train_file, dest_test_file):
	source_file_pointer = open(source_file, "r")
	dest_train_file_pointer = open(dest_train_file, "w")
	dest_test_file_pointer = open(dest_test_file, "w")
	index = 0

	while True:
		temp_string = source_file_pointer.readline()
		if temp_string == "":
			source_file_pointer.close()
			dest_test_file_pointer.close()
			dest_train_file_pointer.close()
			break

		if index % 3 == 0:
			dest_test_file_pointer.write(temp_string)
		else:
			dest_train_file_pointer.write(temp_string)
		index = index + 1

def create_data_file(number_of_lines):
	source_file_pointer = open(master_data_file, "r")
	destination_file_pointer = open(temp_data_file, "w+")
	index = 0
	while True:
		temp_string = source_file_pointer.readline()
		if temp_string == "" or index > number_of_lines:
			source_file_pointer.close()
			destination_file_pointer.close()
			break

		destination_file_pointer.write(temp_string)
		index = index + 1

def create_train_test(number_of_lines, to_vowpal):
	create_data_file(number_of_lines)
	source_file = temp_data_file
	dest_train_file = "data/train.csv"
	dest_test_file = "data/test.csv"
	split_data(source_file, dest_train_file, dest_test_file)
	if to_vowpal:
		convert_to_vw(dest_train_file, "data/train.vw")
		convert_to_vw(dest_test_file, "data/test.vw")



def convert_to_vw(source_file, destination_file):
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

	
		dest_string = label + " | " + "passengers:"+passengers
		dest_string = dest_string + " "+"distance:"+distance
		dest_string = dest_string + " "+"is_weekend:"+is_weekend
		dest_string = dest_string + " "+"start_time:"+start_time
		dest_string = dest_string + " "+"pickup:"+pickup
		dest_string = dest_string + " "+"drop_off:"+drop_off

		destination_file_pointer.write(dest_string)

if __name__ == '__main__':
	create_train_test(100000, True)
