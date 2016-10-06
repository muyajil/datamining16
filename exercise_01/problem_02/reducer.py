import fileinput

A = 1
B = 5
max_count = 5

current_char = None
current_word = None
current_count = 0

char_word_count = 0

for line in fileinput.input():
	[char, word, count] = line.split()
	if(current_char == None):
		[current_char, current_word, current_count] = [char, word, int(count)]
		char_word_count = 1
	elif(current_char == char):
		if(char_word_count <= max_count):
			if(current_word == word):
				current_count += int(count)
			else:
				char_word_count += 1
				if(A <= current_count and current_count <= B):
					print current_word + "\t" + str(current_count)
				current_word = word
				current_count = int(count)
	else:
		current_char = char
		char_word_count = 1
		current_word = word
		current_count = int(count)

if(A <= current_count and current_count <= B):
	print current_word + "\t" + str(current_count)