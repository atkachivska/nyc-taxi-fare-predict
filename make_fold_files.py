def main():

	for index in range(0, 10):
		move_data(index)

fold_file_path = "data/folds/"
consolidated_fold_path = "data/consolidated/"

def move_data_to_fold_file(string, fold_index):
	fold_file = fold_file_path+"fold_file_"+str(fold_index)+".txt"
	pointer = open(fold_file, "a")
	pointer.write(string)
	pointer.close()


def clear_fold_files(folds):
	for fold_index in range(folds):
		fold_file = fold_file_path+"fold_file_"+str(fold_index)+".txt"
		consolidated_train_file = consolidated_fold_path+"train_file_"+str(fold_index)+".txt"
		consolidated_fold_test_file = consolidated_fold_path+"test_file_"+str(fold_index)+".txt"

		pointer = open(fold_file, "w+")
		pointer.write("")
		pointer.close()

		pointer = open(consolidated_train_file, "w+")
		pointer.write("")
		pointer.close()

		pointer = open(consolidated_test_file, "w+")
		pointer.write("")
		pointer.close()


def create_folds(file_name, folds):
	
	source_file_pointer = open(file_name, "r")

	index = 0
	while True:
		line = source_file_pointer.readline()
		if line == "":
			source_file_pointer.close()
			break

		fold_index = index % folds
		move_data_to_fold_file(line, fold_index)
		index = index + 1

def consolidate_folds(folds):

	for fold_index in range(folds):
		consolidated_fold_train_file = consolidated_fold_path+"train_file_"+str(fold_index)+".txt"
		consolidated_fold_test_file = consolidated_fold_path+"test_file_"+str(fold_index)+".txt"
		for inner_index in range(folds):
			fold_file = fold_file_path+"fold_file_"+str(fold_index)+".txt"
			source_pointer = open(fold_file, "r")
			if inner_index == fold_index:
				destination_pointer = open(consolidated_fold_test_file, "a")
			else:
				destination_pointer = open(consolidated_fold_train_file, "a")

			while True:
				line = source_pointer.readline()
				if line == "":
					break
				destination_pointer.write(line)
			source_pointer.close()
			destination_pointer.close()




if __name__ == '__main__':
	folds = 10
	# clear_fold_files(folds)
	# create_folds("data/train.csv", folds)
	consolidate_folds(folds)