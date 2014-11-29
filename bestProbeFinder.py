import numpy as np
from scipy import stats
import math
import csv
from operator import itemgetter

#holds our samples (each person) in a list
sampleList = []
#holds the names of every probe
probeList = []
regressionList = []
class Sample:
    """This class represents one of our samples from the data (one person). """
    
    
    def __init__(self, name, probeDict):
        self.name = name
        self.probeDict = probeDict
        self.regressionValues = []
        
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return str((self.name,self.age,len(self.probeDict)))
    
    def addProbe(self,probeName, probeValue):
        self.probeDict[probeName] = probeValue
        
    def addAge(self,age):
        self.age = age
    
    def getValue(self,probeName):
        return self.probeDict[probeName]
    
    def getAge(self):
        return self.age
        
with open('dataset1.csv', 'rU') as csvfile:
    inFile = csv.reader(csvfile)
    for row in inFile:
        #if reading first row, initialize our samples and their names
        if row[0] == 'ProbeID':
            for i in range (1,len(row)):
                current = Sample(row[i],{})
                sampleList.append(current)
        #if reading age, assign sample ages
        elif row[0] == 'Age':
            for i in range(1,len(row)):
                sampleList[i-1].addAge(float(row[i]))
                
        #if reading probe data, add to proper Sample Object
        else:
            probeName = row[0]
            probeList.append(probeName)
            for i in range(1,len(row)):
                sampleList[i-1].addProbe(probeName,float(row[i]))

for probeName in probeList:
    x = []
    y = []    
    for sample in sampleList:
        x.append(sample.getAge())
        y.append(sample.getValue(probeName))
    xArray = np.array(x)
    yArray = np.array(y)
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x, y)
    regressionList.append((probeName,r_value ** 2))
    
regressionList.sort(key=itemgetter(1))

for i in range(10):
    print regressionList[i]

