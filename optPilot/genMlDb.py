#!/usr/bin/python
'''
Generate database from OPAL optimizer runs.
Here we only use the feasible solutions.

genMlDb.py \
--path=./results \
--filename-postfix=optLinac_40nC.dat_0

         y = f (x)

x == design vectors   (stimuli)
y == objectives       (response)
f == model            (OPAL simulation)
'''
#
import os
import sys
import cPickle as pick
import pyOPALTools.optPilot.OptPilotJsonReader as jsonreader
#
path = ""
outpath = "./"
filename_postfix = "results.json"

def improveName(name):
    name.lstrip().rstrip()        # remove trailing and leading whitespace
    name = name.lstrip('%')       # remove leading %
    name = name.replace(" ", "")  # remove spaces
    name = name.replace('_','\_') # latex handling of underscore
    name = name.replace('\n', '') # remove newlines
    return name

class MlDb:
    def __init__(self,path,filename_postfix):

        trainingSet = []
        dirname = os.path.dirname(path)
        optjson = jsonreader.OptPilotJsonReader(dirname + '/results/')
        
        numGenerations = optjson.getNumOfGenerations()

        for i in range(numGenerations):
            g = optjson.readGeneration(i+1)
            if (i == 0):
                dvarsNames = optjson.getDesignVariables()
                objsNames  = optjson.getObjectives()
                trainingSet.append({'sampleSize':numGenerations, 
                                    'dvarNames':dvarsNames, 
                                    'objNames':objsNames})
            dvars      = optjson.getAllInput()
            ovars      = optjson.getAllOutput()

            trainingSet.append({'dvarValues':dvars,
                                'objValues':ovars})

        print('Write ML-Database ' + filename_postfix+'.pk')    
        pick.dump(trainingSet,open(filename_postfix+'.pk','wb'),-1)

    def load(self,filename):
        with open(filename, 'rb') as f:
            return pick.load(f)

    def getSampleSize(self,data):
        return data[0]['sampleSize']

    def getXDim(self,data):
        return len(data[0]['dvarNames'])
    def getXNames(self,data):
        return data[0]['dvarNames']

    def getYDim(self,data):
        return len(data[0]['objNames'])
    def getYNames(self,data):
        return data[0]['objNames']


def main(argv):
    data = { } 

    for arg in argv:
        if arg.startswith("--path"):
            path = str.split(arg, "=")[1]
    
        elif arg.startswith("--filename-postfix"):
            filename_postfix = str.split(arg, "=")[1]
    
        elif arg.startswith("--outpath"):
            outpath = str.split(arg, "=")[1]
    
    # Generate MlDb from the OPAL simulation
    od = MlDb(path,filename_postfix)

    # Read the data back from pickle file
    data = od.load(filename_postfix+'.pk')
    
    # Show relevant information
    print ('xDim        = ' + str(od.getXDim(data)) + ' -> ' + str(od.getXNames(data)))
    print ('yDim        = ' + str(od.getYDim(data)) + ' -> ' + str(od.getYNames(data)))
    print ('smaple size = ' + str(od.getSampleSize(data)))

#call main
if __name__ == "__main__":    main(sys.argv[1:])
