

def split_train_test(source_file, dest_train_file, dest_test_file):
	source_file_pointer = open(source_file, "r")
	dest_train_file_pointer = open(dest_train_file, "w")
	dest_test_file_pointer = open(dest_test_file, "w")
	index = 0
	while True:
		if index > 30000:
			break
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

if __name__== "__main__":
	split_train_test( "data/master.csv", "data/train.csv", "data/test.csv")