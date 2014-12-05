import numpy as np
import math
import csv
from scipy import stats

x = [] # Telomere Lengths for training set
y = [] # Ages for training set
coeffs = []


with open('data.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
	x.append(int(row[0]))
	y.append(int(row[1])) 


slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

coeffs.append([slope, intercept])

pred = [] # Telomere length for prediction set
age = [] # Correct ages for prediciton set 

with open('pred.csv', 'rU') as predcsv:
    predFile = csv.reader(predcsv)
    for row in predFile:
        pred.append(int(row[0]))
	age.append(int(row[1]))

totalOff = 0
maxOff = 0
for j in xrange(len(pred)):
    exp = len(coeffs) - 1
    prediction = 0
    for i in coeffs:
        prediction += i*(pred[j]**exp)
        exp -= 1
    unsignedOff = abs(age[j] - prediction)
    totalOff += unsignedOff
    if unsignedOff > maxOff:
        maxOff = unsignedOff
    

print("Average error = " + str(totalOff/len(pred)))
print("Maximum error = " + str(maxOff))
