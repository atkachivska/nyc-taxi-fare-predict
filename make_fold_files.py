def main():

	for index in range(0, 10):
		move_data(index)



def move_data(source_file):
	source_file_pointer = open(source_file, "r")

	fold_fi


def move_to_file(file_name):
	file = open(file_name, "r+")
	data_array = []
	for line in file:
		data_array.append(line)

	return data_array





if __name__ == '__main__':
	main()