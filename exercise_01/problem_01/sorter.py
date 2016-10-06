import fileinput
from operator import itemgetter

word_list = []

for line in fileinput.input():
	[word, count] = line.split()
	word_list.append((word,count))

sorted_list = sorted(word_list, key=itemgetter(0))

for (word, count) in sorted_list:
	print word + "\t" + count