import numpy as np
import math
import csv
from scipy import stats 

xList = []
yList = []
dList = []

# Sets how much the weights for predictors change after each prediction
metric = 1.12

# Sets cutoff for minimum r squared value to be considered as a predictor
cutoff = 0.45

# Moves all test data into local variables.  XList holds all test values in list form, YList holds ages in list form
start = False
with open('totalDataDisease.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
	if row[1] == 'Age':
	    yList.append(row[200:])
	elif start:
	    if row[0] == '27579':
		dList.append(row[200:])
	        break
	    xList.append(row[200:])
	start = True

d = []
d = dList[0]
controlBool = []
for element in d:
    if element == '1; control':
        controlBool.append('Normmal')
    elif element == '2; schizophrenia patient':
	controlBool.append('Schiz')
    else:
	controlBool.append(False)



y2 = [float(item) for item in yList[0]]
y = [y2[i] for i in xrange(len(y2)) if controlBool[i] == 'Normal']
yS = [y2[i] for i in xrange(len(y2)) if controlBool[i] == 'Schiz']


# Preparation for calculating all coefficients for separate predictors
coeffs = []
coeffsS = []
measure = []
measureS = []

r_max = 0
p_used = 0
# Looping through each separate data set and calculating coefficients for it's predictor
for j in xrange(len(xList)):
    x = []
    xS = []
    for v in xrange(len(xList[j])):
	if controlBool[v] == 'Normal':
            if xList[j][v] != 'NA' and xList[j][v] != '':
                x.append(float(xList[j][v]))
            else:
    	        x.append(float(0))
	elif controlBool[v] == 'Schiz':
	    if xList[j][v] != 'NA' and xList[j][v] != '':
                xS.append(float(xList[j][v]))
            else:
    	        xS.append(float(0))


    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    slopeS, interceptS, r_valueS, p_valueS, std_errS = stats.linregress(xS, yS)
    coeffs.append([slope, intercept])
    coeffsS.append([slopeS, interceptS])
    if r_value**2 - cutoff > 0:
	p_used += 1
        measure.append(r_value**2-cutoff)
    else:
	measure.append(0)
    if r_value**2 > r_max:
	r_max = r_value**2
    
    if r_valueS**2 - cutoff > 0:
        measureS.append(r_valueS**2-cutoff)
    else:
	measureS.append(0)

print p_used
print r_max

# Grabbing data for predictor

predList = []
ageList = []
dPredList = []
start = False

with open('totalDataDisease.csv', 'rU') as predcsv:
    predFile = csv.reader(predcsv)
    for row in predFile:
        if row[1] == 'Age':
	    ageList.append(row[2:200])
	elif start:
	    if row[0] == '27579':
		dPredList.append(row[2:200])
	        break
	    predList.append(row[2:200])
	start = True 

# Isolates data from only controls so that we don't use diseased patients data

d = []
d = dPredList[0]
controlBool = []
for element in d:
    if element == '1; control':
        controlBool.append('Normmal')
    elif element == '2; schizophrenia patient':
	controlBool.append('Schiz')
    else:
	controlBool.append(False)
    


age = [float(ageList[0][j]) for j in xrange(len(ageList[0])) if controlBool[j] == 'Normal']
ageS = [float(ageList[0][j]) for j in xrange(len(ageList[0])) if controlBool[j] == 'Schiz']


predAge = []
predAgeS = []

# Setting up predAge - the list of predicted ages for each individual

for m in xrange(len(age)):
    predAge.append([])
for m in xrange(len(ageS)):
    predAgeS.append([])

# For each predictor, predict for every individual and store it in their proper list in predAge

for k in xrange(len(predList)):
    pred = []
    predS = []
    for v in xrange(len(predList[k])):
        if controlBool[v] == 'Normal':
            if predList[k][v] != 'NA' and predList[k][v] != '':
		pred.append(float(predList[k][v]))
            else:
               	pred.append(float(0))
	elif controlBool[v] == 'Schiz':
	    if xList[j][v] != 'NA' and xList[j][v] != '':
                predS.append(float(xList[j][v]))
            else:
    	        predS.append(float(0))

    for j in xrange(len(pred)):
	prediction = coeffs[k][0]*pred[j] + coeffs[k][1]
	# Puts limits on age ranges you can guess
	if prediction < 3:
	    prediction = 3
	elif prediction > 85:
	    prediction = 85
	predAge[j].append(prediction)

    for j in xrange(len(predS)):
	prediction = coeffsS[k][0]*predS[j] + coeffsS[k][1]
	# Puts limits on age ranges you can guess
	if prediction < 3:
	    prediction = 3
	elif prediction > 85:
	    prediction = 85
	predAgeS[j].append(prediction)

        

# Use a simple fitness function/genetic algorithm to train weights on predictions
    
finalList = []
finalListS = []
for f in xrange(len(predAge)):
    runSum = 0
    for g in xrange(len(predAge[f])):
        runSum += predAge[f][g] * measure[g]
    if len(measure) > 0:
        predValue = float(runSum)/float(sum(measure))
        totOff = abs(age[f] - predValue)
        for g in xrange(len(measure)):
	    if measure[g] != 0:
	        if abs(age[f] - predAge[f][g]) < totOff:
		    measure[g] *= metric
	        else: 
		    measure[g] *= 1/float(metric)

for f in xrange(len(predAgeS)):
    runSum = 0
    for g in xrange(len(predAgeS[f])):
        runSum += predAgeS[f][g] * measureS[g]
    if len(measureS) > 0:
        predValue = float(runSum)/float(sum(measureS))
        totOff = abs(ageS[f] - predValue)
        for g in xrange(len(measureS)):
	    if measureS[g] != 0:
	        if abs(ageS[f] - predAgeS[f][g]) < totOff:
		    measureS[g] *= metric
	        else: 
		    measureS[g] *= 1/float(metric)

# Actually calculate predictions based on found weights

for f in xrange(len(predAge)):
    runSum = 0
    for g in xrange(len(predAge[f])):
        runSum += predAge[f][g] * measure[g]
    if len(measure) > 0:
        predValue = float(runSum)/float(sum(measure))
        finalList.append(predValue) 

for f in xrange(len(predAgeS)):
    runSum = 0
    for g in xrange(len(predAgeS[f])):
        runSum += predAgeS[f][g] * measureS[g]
    if len(measureS) > 0:
        predValue = float(runSum)/float(sum(measureS))
        finalListS.append(predValue)


# Compute statistics about prediction success

totalsum = 0
maxDif = 0
for i in xrange(len(finalList)):
    dif = abs(finalList[i]-age[i])
    totalsum += dif
    if maxDif < dif:
	maxDif = dif

for i in xrange(len(finalListS)):
    dif = abs(finalListS[i]-ageS[i])
    totalsum += dif
    if maxDif < dif:
	maxDif = dif

average = float(totalsum)/float(len(finalList) + len(finalListS))

newSum = 0

for i in xrange(len(finalList)):
    dif = (abs(finalList[i]-age[i]) - average)**2
    newSum += dif

for i in xrange(len(finalListS)):
    dif = (abs(finalListS[i]-ageS[i]) - average)**2
    newSum += dif


stdDev = math.sqrt(float(newSum)/float(len(finalList) + len(finalListS)))

print("Maximum Off: " + str(maxDif))
print("Average Off: " + str(average))
print("Standard Dev Off: " + str(stdDev))
