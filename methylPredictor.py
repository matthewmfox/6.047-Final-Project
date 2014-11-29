import numpy as np
import math
import csv

xList = []
yList = []

# Moves all test data into local variables.  XList holds all test values in list form, YList holds ages in list form
start = False
with open('dataset1.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
	if row[0] == 'Age':
	    yList.append(row[1:12])
	    break
	if start:
	    xList.append(row[1:12])
	start = True

# Preparation for calculating all coefficients for separate predictors
coeffs = []
y = [float(item) for item in yList[0]]

# Looping through each separate data set and calculating coefficients for it's predictor
for j in xrange(len(xList)):
    x = [float(item) for item in xList[j]]

    value = 0
    mini = -1
    for i in range(1,4):
        if np.sum((np.polyval(np.polyfit(x, y, i), x) - y)**2) < (mini/2) or mini == -1:
            value = i
    	mini = np.sum((np.polyval(np.polyfit(x, y, i), x) - y)**2)
    coeffs.append(np.polyfit(x,y,value))


# Grabbing data for predictor

predList = []
ageList = []
start = False

with open('dataset1.csv', 'rU') as predcsv:
    predFile = csv.reader(predcsv)
    for row in predFile:
        if row[0] == 'Age':
	    ageList.append(row[13:])
	    break
	if start:
	    predList.append(row[13:])
	start = True 

age = [float(item) for item in ageList[0]]

predAge = []

for m in xrange(4):
    predAge.append([])

for k in xrange(len(predList)):

    pred = [float(item) for item in predList[k]]

    totalOff = 0
    maxOff = 0
    for j in xrange(len(pred)):
        exp = len(coeffs[k]) - 1
        prediction = 0
        for i in coeffs[k]:
            prediction += i*(pred[j]**exp)
            exp -= 1
	predAge[j].append(int(prediction))
        unsignedOff = abs(age[j] - prediction)
        totalOff += unsignedOff
        if unsignedOff > maxOff:
            maxOff = unsignedOff
        
    
    #print("Average error = " + str(totalOff/len(pred)))
    #print("Maximum error = " + str(maxOff))


predAge = [sum(item)/len(item) for item in predAge]
print predAge
