from scipy.optimize import brenth
from decimal import Decimal
import bisect

estimates = []
goal_estimate = 0.85

for i in range(1,1024):
	for j in range(1,1024):
		if(i*j < 300 or i*j > 1024):
			break
		zero = brenth((lambda x: 1-(1-x**i)**j - 0.5), 0, 1)
		estimates.append((zero, i, j))
		#print str(i) + "\t" + str(j) + "\t" + str(zero)
		#if(abs(Decimal(best_estimate[0])-Decimal(goal_estimate)) > abs(Decimal(zero)-Decimal(goal_estimate))):
		#	best_estimate = (zero, i, j)
estimates.sort(key=(lambda x: abs(x[0] - goal_estimate)))
print ""
print "Top 10 Estimates"
print ""
for i in range(10):
	print str(i+1) + ":\t" + str(estimates[i][1]) + "\t" + str(estimates[i][2]) + "\t" + str(estimates[i][0])
