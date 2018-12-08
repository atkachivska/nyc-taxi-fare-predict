import random

def get_number_of_lines_in_file(source_file):
	source_pointer = open(source_file, "r")

	lines = 0
	while True:
		string = source_pointer.readline()
		if string == "":
			break
		else:
			lines = lines + 1

	return lines

def get_random_lines_for_knn(source_file, destination_file, no_of_lines, lines_to_select):
	source_pointer = open(source_file, "r")
	dest_pointer = open(destination_file, "w")
	temp = lines_to_select

	while temp > 0:
		index = random.randint(0, no_of_lines-1)
		source_line = source_pointer.readline(index)
		dest_pointer.write(source_line)
		temp = temp - 1


if __name__== "__main__":
	lines = get_number_of_lines_in_file("data/master_before_knn.csv")
	get_random_lines_for_knn("data/master_before_knn.csv", "data/knn_source.csv",  lines, 10000)
