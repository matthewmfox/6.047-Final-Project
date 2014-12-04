import numpy as np
import math
import csv
from scipy import stats 

xList = []
yList = []

# Moves all test data into local variables.  XList holds all test values in list form, YList holds ages in list form
start = False
with open('totalData.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
	if row[1] == 'Age':
	    yList.append(row[2:100] + row[300:])
	elif start:
	    xList.append(row[2:100] + row[300:])
	    if row[1] == 'cg27665659':
	        break
	start = True




# Preparation for calculating all coefficients for separate predictors
coeffs = []
measure = []
y = [float(item) for item in yList[0]]

r_max = 0
p_used = 0
# Looping through each separate data set and calculating coefficients for it's predictor
for j in xrange(len(xList)):
    x = []
    for item in xList[j]:
        if item != 'NA' and item != '':
            x.append(float(item))
        else:
	    x.append(float(0))


    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    coeffs.append([slope, intercept])
    if r_value**2 - 0.45 > 0:
	p_used += 1
        measure.append(r_value**2-0.45)
    else:
	measure.append(0)
    if r_value**2 > r_max:
	r_max = r_value**2

print p_used
print r_max


# Grabbing data for predictor

predList = []
ageList = []
start = False

with open('totalData.csv', 'rU') as predcsv:
    predFile = csv.reader(predcsv)
    for row in predFile:
        if row[1] == 'Age':
	    ageList.append(row[100:300])
	elif start:
	    predList.append(row[100:300])
	    if row[1] == 'cg27665659':
	        break
	start = True 

age = [float(item) for item in ageList[0]]

predAge = []

# Setting up predAge - the list of predicted ages for each individual

for m in xrange(len(predList[0])):
    predAge.append([])

# For each predictor, predict for every individual and store it in their proper list in predAge

for k in xrange(len(predList)):
    pred = []
    for item in predList[k]:
        if item != 'NA' and item != '':
            pred.append(float(item))
        else:
	    pred.append(float(0))

    printed = False
    for j in xrange(len(pred)):
	prediction = coeffs[k][0]*pred[j] + coeffs[k][1]
	if prediction < 3:
	    prediction = 3
	elif prediction > 85:
	    prediction = 85
	prediction *= measure[k]
	if printed == False:
	    #if measure[k] != 0:
	        #print float(prediction)/float(measure[k])
	    printed = True
	predAge[j].append(prediction)
        

# Calculate their age prediction based on the weighted predictions
    
finalList = []
for f in xrange(len(predAge)):
    finalList.append(float(sum(predAge[f]))/float(sum(measure)))

#print finalList
#print age

totalsum = 0
maxDif = 0
for i in xrange(len(finalList)):
    dif = abs(finalList[i]-age[i])
    totalsum += dif
    if maxDif < dif:
	maxDif = dif

print("Maximum Off: " + str(maxDif))
print("Average Off: " + str(totalsum/len(finalList)))
