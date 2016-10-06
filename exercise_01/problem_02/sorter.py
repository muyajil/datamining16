import fileinput
from operator import itemgetter

word_list = []

for line in fileinput.input():
	[char, word, count] = line.split()
	word_list.append((char,word,count))

sorted_list = sorted(word_list, key=itemgetter(1))

for (char, word, count) in sorted_list:
	print char + "\t" + word + "\t" + count