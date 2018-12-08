def main():

	for index in range(0, 10):
		move_data(index)



def move_data(fold_index):


	fold_data_path = "./data/folds/"

	training_data_file = "training_data_"+str(fold_index)+".txt"
	testing_data_file = "testing_data_"+str(fold_index)+".txt"


	testing_data_array = []
	training_data_array = []

	for index in range(0, 10):
		file_string = fold_data_path+"/"+"fold_file_"+str(index)+".txt"
		if index == fold_index:
			testing_data_array.extend(move_to_file(file_string))
		else:
			training_data_array.extend(move_to_file(file_string))


	consolidated_data_path = "/Users/praveenoak/Desktop/svm/folds/consolidated"

	train_data_name = consolidated_data_path+"/"+"training_set_"+str(fold_index)+".txt"
	test_data_name = consolidated_data_path+"/"+"testing_set_"+str(fold_index)+".txt"

	print_to_file(train_data_name, training_data_array)
	print_to_file(test_data_name, testing_data_array)
	

def print_to_file(file_name, array):
	file = open(file_name, "w+")
	for data in array:
		file.write(data)


def move_to_file(file_name):
	file = open(file_name, "r+")
	data_array = []
	for line in file:
		data_array.append(line)

	return data_array





if __name__ == '__main__':
	main()