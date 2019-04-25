import numpy as np
import sys
import os
from datetime import datetime
from bisect   import bisect_left
from opal import load_dataset, filetype

if sys.version_info[0] < 3:
  # Python 2
  import cPickle as pick
else:
  # Python 3
  import pickle as pick

from opal.parser.OptimizerParser import OptimizerParser
#
#from utilities import SDDSParser


def strToFloat(in_array):
  out_array=[]
  for in_row in in_array:
    out_row = [float(i) for i in in_row]
    out_array.append(out_row)
  return out_array



# From https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
def findClosestIndex(myList, myNumber):
  """
  Assumes myList is sorted. Returns closest index to myNumber.
  
  If two numbers are equally close, return the smallest number.
  """
  pos = bisect_left(myList, myNumber)
  if pos == 0:
    return 0
  if pos == len(myList):
    return pos - 1
  before = myList[pos - 1]
  after  = myList[pos]
  if after - myNumber < myNumber - before:
    return pos
  else:
    return pos - 1

def substring_after(s, delim):
    return s.partition(delim)[2]

def substring_before(s, delim):
    return s.partition(delim)[0]

def checkBounds(data, keys):
    #nxs = number of x variables
    nxs  = len(keys)
    #Print bounds 
    for j in range(0, nxs):
        print('Now printing bounds of bad points:')
        print("max of "+ keys[j] + '= '+ str(max(data[0]['dvarValues'][:,j])))
        print("min of "+ keys[j] + '= '+ str(min(data[0]['dvarValues'][:,j])))
        print('\n')

def buildBounded(pickle, baseFN):
    #Build a data base using simulations within bounds given
    dbr = mldb()
    dbr.load(pickle)
    ulb = dbr.getBounds()
    
    keys = dbr.getXNames()   
    n    = len(keys) 
    lb   = np.zeros((1, n))
    ub   = np.zeros((1, n))
    #Make array with upper bounds (ub) 
    #and lower bounds (lb)    
    for i, key in enumerate(keys):
        lb[0, i] = ulb[key][0]         
        ub[0, i] = ulb[key][1]
    print(lb)
    print(ub) 
    totalgen  = dbr.getNumberOfSamples()  
    bounded   = []
    unbounded = [] 
    xvec  = np.zeros((1, n))
    bxvec = np.zeros((1, n))
    objsNames  = dbr.getYNames()
    nobjs = len(objsNames)
    yvec  = np.zeros((1, len(objsNames)))
    byvec = np.zeros((1, len(objsNames)))

    #Loop through each generation
    for gen in range(0, totalgen):
        nsims  = dbr.getSampleSize(i=gen)
        gxvec  = np.zeros((1, n))
        gyvec  = np.zeros((1, len(objsNames)))
        #Save extra info            
        if (gen == 0):
            bounded.append({'sampleSize':totalgen,
                'dvarNames' :keys,
                'objNames'  :objsNames,
                'bounds'    :ulb})

        #Loop through each simulation in gen 
        for x in range(0, nsims):
            xvals  = (dbr.getDVarVec(gen,x)).reshape((1,n))
            ovals  = (dbr.getObjVec(gen,x)).reshape((1,nobjs))
            testlb = np.less_equal(xvals, lb)
            testub = np.greater_equal(xvals, ub)
            #Check if xvals <= lb or xvlas >= ub
            if (any(testlb[0]) == True) or (any(testub[0]) == True):  
                bxvec = np.append(bxvec, xvals, axis=0)
                byvec = np.append(byvec, ovals, axis=0)
            #Check if xvlas within all bounds
            elif (all(testlb[0]) == False) and (all(testub[0]) == False):
                #print(testlb[0])
                #print(testub[0])
                #print(xvals)
                xvec = np.append(xvec, xvals, axis=0)
                yvec = np.append(yvec, ovals, axis=0)
                gxvec = np.append(gxvec, xvals, axis=0)
                gyvec = np.append(gyvec, ovals, axis=0)

            else:
                print('Mistake, xvals not in boundaries expected.')
                print('Don\'t trust the database.')
        
        gxvec = gxvec[1:,:]
        gyvec = gyvec[1:,:]
        #Saving good pts per generation
        bounded.append({'dvarValues':gxvec,'objValues' :gyvec})
        print('generation # '+ str(gen+1) +', Number of sims:'+ str(nsims) + ', Number of bounded sims: ' + str(np.size(gxvec[:,0])), end='\r', flush=True)
    #Getting rid of place holders
    xvec  = xvec[1:,:]
    yvec  = yvec[1:,:]
    bxvec = bxvec[1:,:]
    byvec = byvec[1:,:]
    #Saving all data in one entry
    bounded.append({'allDvarValues':xvec, 'allObjValues':yvec})
    #Saving all bad points, looses generation info
    unbounded.append({'dvarValues':bxvec, 'objValues' :byvec})

    print('# bad pts:', str(np.size(bxvec[:,0])),', # good pts:', str(np.size(xvec[:,0])))
    if (np.size(bxvec[:,0]) > 0):
        badbounds = checkBounds(unbounded, keys)

    filename = baseFN+'-bounded.pk'
    print('Write ML-Database ' + filename)
    pick.dump(bounded,open(filename,'wb'),-1)

class mldb:
 
    def __init__(self, descr=''):
        print('OPAL ML Database Generator \x1b[6;30;42m' + descr + '\x1b[0m')

    def build(self,filename_postfix, path):
        self.trainingSet = []
        optjson = OptimizerParser(path + '/')
        
        numGenerations = optjson.getNumOfGenerations()

        for i in range(numGenerations):
            g = optjson.readGeneration(i+1)
            if (i == 0):
                dvarsNames = optjson.getDesignVariables()
                objsNames  = optjson.getObjectives()
                bounds     = optjson.getBounds()
                self.trainingSet.append({'sampleSize':numGenerations, 
                                         'dvarNames' :dvarsNames, 
                                         'objNames'  :objsNames,
                                         'bounds'    :bounds})
            dvars      = optjson.getAllInput()
            ovars      = optjson.getAllOutput()

            self.trainingSet.append({'dvarValues':dvars,
                                     'objValues' :ovars})

        self.writeDB(filename_postfix)

    def buildFromSampler(self, jsonFN, root, yNames, statBaseFn):
        '''
        Build training set from an OPAL sampler run
        '''
        ds = load_dataset(root, fname=jsonFN)
        
        self.trainingSet = []        
        x = []
        y = []
        fns = []

        for ind in range(0,ds.size):
            statData=load_dataset(root, fname=str(ind)+'/'+statBaseFn+'.stat')
            fns.append(str(ind)+'/'+statBaseFn+'.stat')
            xstr = ""
            ystr = ""
            for dvar in ds.design_variables:
                xstr += dvar+"="+ds.getData(dvar,ind=ind)+" "
            x.append(xstr)
            for obj in yNames:
                ystr += str(statData.getData(obj)[-1])+" " 
            y.append(ystr)
        
        lDataSets = len(x)
        xDim      = len(x[0].split())
        yDim      = len(yNames)
        
        '''the following is a copy from buildFromSDDS '''
               
        xNames   = []
        xValues  = []
        xall = x[0].split()
        for i in range(xDim):    
            xNames.append(substring_before(xall[i], '='))
            xValues.append(substring_after(xall[i], '='))
        
        # design variables
        dvarsNames = xNames
        # object variables
        objsNames  = yNames

        dvars = []
        ovars = []
        for i in range(lDataSets):
            xall = x[i].split()
            xi = []
            for j in range(xDim):
                xi.append(substring_after(xall[j], '='))
            dvars.append(xi)
            ovars.append(y[i])
        
        numGenerations = 1

        self.trainingSet.append({'sampleSize':numGenerations,
                                 'dvarNames' :dvarsNames,
                                 'objNames'  :objsNames,
                                 'dataFiles' :fns})

        self.trainingSet.append({'dvarValues':dvars,
                                 'objValues' :ovars})

        dataFileName = 'test.huuuu'
        self.writeDB(statBaseFn)
        
    def buildFromSDDS(self,baseFN, root, yNames):
        '''
        Build training set from sdds (simulation) data obtained with for example OPAL
        The dataDescriptionFile will define the input (aka design) and output (aka object) variables
        '''
        self.trainingSet = []
        
        p   = SDDSParser()
        x   = []
        y   = []
        fns = []

        cwd       = os.getcwd()
        os.chdir(root)        
        (x,y,fns) = p.collectStatFileData(baseFN, '.', yNames)
        os.chdir(cwd)

        lDataSets = len(x)
        xDim      = len(x[0].split())
        yDim      = len(yNames)
        xNames   = []
        xValues  = []
        
        print('dim(x)= ', xDim, 'dim(y)= ', yDim, ' #datapoints= ',lDataSets)
        
        xall = x[0].split()
        for i in range(xDim):    
            xNames.append(substring_before(xall[i], '='))
            xValues.append(substring_after(xall[i], '='))
        
        # design variables
        dvarsNames = xNames
        # object variables
        objsNames  = yNames

        dvars = []
        ovars = []
        for i in range(lDataSets):
            xall = x[i].split()
            xi = []
            for j in range(xDim):
                xi.append(substring_after(xall[j], '='))
            yi = []
            for j in range(len(yNames)): 
                yi.append(y[i][j][-1])  
                
            dvars.append(xi)
            ovars.append(yi)
        
        #print(str(ovars[0])+'= f('+str(dvars[0])+')' )
               
        # Add to training set
        # Treat everything as one generation
        numGenerations = 1

        self.trainingSet.append({'sampleSize':numGenerations,
                                 'dvarNames' :dvarsNames,
                                 'objNames'  :objsNames,
                                 'dataFiles' :fns})

        self.trainingSet.append({'dvarValues':dvars,
                                 'objValues' :ovars})

        dataFileName = 'test.huuuu'
        self.writeDB(baseFN)


    def buildASCII(self,path,dataDescriptionFile,dataFileName,interlockFileName):
        '''
        Build training set from archiver data obtained with the ArchiveExport command
        The dataDescriptionFile will define the input (aka design) and output (aka object) variables
        '''
        self.trainingSet = []
        # Number of header lines
        nrHeaderLines = 4
        # Filling number that replaces bad numbers
        # Lines with this number will be removed
        fillingNumber = 12356789

        # read dataDescriptionFile
        dataDescription = np.genfromtxt(path + '/' + dataDescriptionFile,
                                        dtype=[('input','U1'),('name','|U30'),('unit','|S8')],
                                        comments='#')

        # design variables
        dvarsNames = [pv['name'] for pv in dataDescription if pv['input']=='x']
        # object variables
        objsNames  = [pv['name'] for pv in dataDescription if pv['input']=='y']

        # read data (to be put in separate class)

        # match with header data file
        if sys.version_info[0] < 3:
          f = open(dataFileName)
        else:
          f = open(dataFileName, errors='ignore')
        for i in range(0,nrHeaderLines):
            header = f.readline()
        f.close()

        # Header has following format: '# Time name1 [unit1] name2 [unit2] etc.
        # We are interested in names only.
        # Problem: Unit can have spaces
        # Solution: skip first two words and those that have a bracket
        dataNames = [name for name in header.split()[2:] if not ('[' in name or ']' in name)]

        if not dataNames:
          print('no header found in data')
          return

        # get variables in data
        # add 2 to column number since first column is data and second time
        # zip(*) operation 'inverses' the lists
        dcols, dvarsNamesInData = zip(*[(index+2,name) for index,name in enumerate(dataNames) if name in dvarsNames])
        ocols, objsNamesInData  = zip(*[(index+2,name) for index,name in enumerate(dataNames) if name in objsNames])

        # print variables not in data
        dvarsNamesNotInData = [name for name in dvarsNames if name not in dataNames]
        objsNamesNotInData  = [name for name in objsNames  if name not in dataNames]

        if dvarsNamesNotInData:
          print('WARNING: Design variables not in data', dvarsNamesNotInData)
          
        if objsNamesNotInData:
          print('WARNING: Objectives not in data',       objsNamesNotInData)

        # Input data
        # Need to skip lines with "#N/A" and "<no data>"
        dvars = np.genfromtxt(dataFileName,
                              usecols     = dcols,
                              skip_header = nrHeaderLines,
                              comments    = None,
                              filling_values = fillingNumber)

        # Output data
        ovars = np.genfromtxt(dataFileName,
                              usecols     = ocols,
                              skip_header = nrHeaderLines,
                              comments    = None,
                              filling_values = fillingNumber)

        # Timing data
        str2date = lambda x: datetime.strptime(x.decode("utf-8"), '%m/%d/%Y')
        # Strip nanosecond info
        str2time = lambda x: datetime.strptime(x.decode("utf-8")[:-3], '%H:%M:%S.%f')

        timevars = np.genfromtxt(dataFileName,
                                 usecols     = {0,1},
                                 skip_header = nrHeaderLines,
                                 dtype       = None,
                                 converters  = {0:str2date, 1:str2time})

        # Add date + time into single datetime
        tvars = np.array([datetime.combine(date.date(),time.time()) for (date,time) in zip(timevars[:,0],timevars[:,1])])

        # remove rows with fillingNumber in dvars
        mask = ~(dvars==fillingNumber).any(1)
        if sum(~mask):
            print (sum(~mask), 'rows will be removed with non-complete design data')

        dvars = dvars[mask]
        ovars = ovars[mask]
        tvars = tvars[mask]

        # remove rows with fillingNumber in ovars
        mask = ~(ovars==fillingNumber).any(1)
        if sum(~mask):
            print (sum(~mask), 'rows will be removed with non-complete object data')

        dvars = dvars[mask]
        ovars = ovars[mask]
        tvars = tvars[mask]

        print (sum(mask), 'rows are left')

        # Interlock file
        if interlockFileName:
            # Procedure:
            # Add one or each interlock to objNames (proposal ILOCK-xxx)
            # Make zero vectors for each interlock
            # Use interlock timestamp to add 1's
            # Add vectors to objValues
            
            str2date = lambda x: datetime.strptime(x.decode("utf-8"), '%Y-%m-%d')
            # Now no nanosecond info
            str2time = lambda x: datetime.strptime(x.decode("utf-8"), '%H:%M:%S.%f')
            interlockvars = np.genfromtxt(interlockFileName,
                                          usecols     = {0,1},
                                          dtype       = None,
                                          converters  = {0:str2date, 1:str2time})
 
            # Add date + time into single datetime
            interlocktime = [datetime.combine(date.date(),time.time()) for (date,time) in zip(interlockvars[:,0],interlockvars[:,1])]
            # For each interlock time find corresponding tvar time
            # We know that dates are sorted so we can use binary search
            interlocks = np.zeros(len(tvars))

            for time in interlocktime:
                interlocks[findClosestIndex(tvars,time)] = 1

            # If interlock file has larger range than data file first and last interlock might falsely be 1
            # Reset to 0
            interlocks[0]  = 0
            interlocks[-1] = 0

            # Add to objectives
            objsNamesInData += ('ILOCK',)
            # Reallocating ovars, is there a more efficient way?
            ovars = np.column_stack((ovars,interlocks));

        # Add to training set
        # Treat everything as one generation
        numGenerations = 1

        self.trainingSet.append({'sampleSize':numGenerations,
                                 'dvarNames' :dvarsNamesInData,
                                 'objNames'  :objsNamesInData})
        self.trainingSet.append({'dvarValues':dvars,
                                 'objValues' :ovars,
                                 'times'     :tvars})

        self.writeDB(dataFileName)


    def writeDB(self,filename_postfix):

        print('Write ML-Database ' + filename_postfix+'.pk')    
        pick.dump(self.trainingSet,open(filename_postfix+'.pk','wb'),-1)

    def load(self,filename):
        with open(filename, 'rb') as f:
            if sys.version_info[0] < 3:
                self.trainingSet = pick.load(f)
            else:
                self.trainingSet = pick.load(f,encoding='latin1')

    def getSampleSize(self,i=0):
        return len(self.trainingSet[i+1]['dvarValues'])

    def getNumberOfSamples(self):
        return self.trainingSet[0]['sampleSize']

    def getXDim(self):
        return len(self.trainingSet[0]['dvarNames'])

    def getXNames(self):
        return self.trainingSet[0]['dvarNames']

    def getYDim(self):
        return len(self.trainingSet[0]['objNames'])
    
    def getYNames(self):
        return self.trainingSet[0]['objNames']

    def getAllDvar(self,gen):
        return self.trainingSet[gen+1]['dvarValues'][:]

    def getAllObj(self,gen):
        return self.trainingSet[gen+1]['objValues'][:]

    def getAllDvarData(self):
        data = self.getAllDvar(0)
        for i in range(1,self.getNumberOfSamples()):
          data = np.append(data, self.getAllDvar(i), axis=0)
        data = strToFloat(data)    
        nQoIs   = len(self.getXNames())
        data = np.asarray(data)
        data = data[:,:nQoIs]
        return data

    def getAllObjData(self):
        data = self.getAllObj(0)
        for i in range(1,self.getNumberOfSamples()):
            data = np.append(data, self.getAllObj(i), axis=0)
        data = strToFloat(data)    
        nQoIs   = len(self.getYNames())
        data = np.asarray(data)
        data = data[:,:nQoIs]
        return data




    def getDVarVec(self,gen,indiv):
        return self.trainingSet[gen+1]['dvarValues'][indiv]

    def getObjVec(self,gen,indiv):
        return self.trainingSet[gen+1]['objValues'][indiv]

    def getTimes(self,gen,indiv):
        return self.trainingSet[gen+1]['times'][indiv]
    
    def getBounds(self):
        return self.trainingSet[0]['bounds']

    def printOverview(self):
        if (self.trainingSet):
            # Show relevant information
            print ('xDim        = ' + str(self.getXDim()) + ' -> ' + str(self.getXNames()))
            print ('yDim        = ' + str(self.getYDim()) + ' -> ' + str(self.getYNames()))
            print ('generations = ' + str(self.getNumberOfSamples()))
            
            samples=0
            for i in range(self.getNumberOfSamples()):
                s = self.getSampleSize(i)
                samples += s 

            print('Data points  = ' + str(samples))

            # Example for a query:
            x = []
            y = []
            x = self.getDVarVec(0,0)
            y = self.getObjVec(0,0)
            
            print('Show first dataset from generation 0: y = f(x)')
            print (str(y)+ ' = f('+str(x)+')')
        else:
            print('Load data first')
            sys.exit()


#def main(argv):
#    readAscii           = False # read ASCII or JSON
#    filename_postfix    = "results.json"
#    dataDescriptionFile = "dataDescr.txt"
#    interlockFile       = None
#    path                = ""
#
#    for arg in argv:
#        if arg.startswith("--path"):
#            path = str.split(arg, "=")[1]    
#        elif arg.startswith("--filename-postfix"):
#            filename_postfix = str.split(arg, "=")[1]
#        elif arg.startswith("--dataDescription"):
#            dataDescriptionFile = str.split(arg, "=")[1]
#        elif arg.startswith("--ascii"):
#            readAscii=True
#        elif arg.startswith("--interlock"):
#            interlockFile = str.split(arg, "=")[1]
#
#    dbO = MlDb()    
#
#    # Generate and save MlDb from the OPAL simulation
#    if readAscii:
#        dbO.buildASCII(path, dataDescriptionFile, filename_postfix, interlockFile)
#    else:
#        # JSON
#        dbO.build(path,filename_postfix)
#
#    # read the data from the MlDb
#    dbO.load(filename_postfix+'.pk')  
#
#    # 
#    #
#    # iterate over all generations and individuals
#    # this can be used to create the neural net.
#    #
#
#    x = []
#    y = []
#    for i in range(dbO.getNumberOfSamples()):
#        for j in range(dbO.getSampleSize(i)):
#            x = dbO.getDVarVec(i,j)
#            y = dbO.getObjVec(i,j)
#   
#    dbO.printOverview()

#call main
#if __name__ == "__main__":    main(sys.argv[1:])
