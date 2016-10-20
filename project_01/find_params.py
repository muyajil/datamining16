from scipy.optimize import brenth
from decimal import Decimal

best_estimate = (10000,0,0)
goal_estimate = 0.85

for i in range(1,1024):
	for j in range(1,1024):
		if(i*j > 1024):
			break
		zero = brenth((lambda x: 1-(1-x**i)**j - 0.5), 0, 1)
		print str(i) + "\t" + str(j) + "\t" + str(zero)
		if(abs(Decimal(best_estimate[0])-Decimal(goal_estimate)) > abs(Decimal(zero)-Decimal(goal_estimate))):
			best_estimate = (zero, i, j)
print ""
print "Best Estimate"

print str(best_estimate[1]) + "\t" + str(best_estimate[2]) + "\t" + str(best_estimate[0])