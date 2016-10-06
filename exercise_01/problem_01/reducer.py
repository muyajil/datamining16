import fileinput

current_word = None
current_count = 0

for line in fileinput.input():
	[word, count] = line.split()
	if(current_word == None):
		current_word = word
		current_count = int(count)
	elif(current_word == word):
		current_count += int(count)
	else:
		print current_word + "\t" + str(current_count)
		current_word = word
		current_count = int(count)

print current_word + "\t" + str(current_count)