import numpy as np
import math
import csv

x = []
y = []
with open('data.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
	x.append(int(row[0]))
	y.append(int(row[1])) 


value = 0
mini = -1
for i in xrange(4):
    if np.sum((np.polyval(np.polyfit(x, y, i), x) - y)**2) < (mini/10) or mini == -1:
        value = i
	mini = np.sum((np.polyval(np.polyfit(x, y, i), x) - y)**2)

coeffs = np.polyfit(x,y,value)

pred = []
age = []

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
