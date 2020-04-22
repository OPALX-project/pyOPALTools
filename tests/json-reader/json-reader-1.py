from opal.parser.OptimizerParser import OptimizerParser as optreader

import sys,os


try:
    
    # 1. Find all .json files of a directory, e.g. "./"
    optjson = optreader("./data/")
    optjson.parse()
    print ( "Read generation ", sys.argv[1])
    # 2. Read in a generation file, e.g. 450  
    optjson.readGeneration(int(sys.argv[1]))
    
    # 3. Obtain an individual
    print ( optjson.getDesignVariables() )
    print ( optjson.getObjectives())
#    var = optjson.getVariableNames()[1]
#    print ( optjson.getIndividual(1, var) )
    
    # raise error
#    print ( optjson.getIndividual(1, "bla") )

except:
    print ( sys.exc_info()[1] )
