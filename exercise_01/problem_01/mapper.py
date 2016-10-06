import fileinput
import re

regex = re.compile('[^a-zA-Z]')

for line in fileinput.input():
	alpha_line = regex.sub(' ', line).lower()
	words = alpha_line.split()
	for word in words:
		print word + "\t" + str(1)