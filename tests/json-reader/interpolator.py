from pyOPALTools.optPilot import OptPilotJsonReader as optreader
import sys
import numpy as np

from scipy.interpolate import LinearNDInterpolator

from pyOPALTools.optPilot import Interpolator as inpl

try:
    
    # 1. Find all .json files of a directory, e.g. "./"
    optjson = optreader.OptPilotJsonReader("./data/")
    
    length = len( optjson.getDesignVariables() )
    coords = np.empty( (0, length), float)
    
    length = len( optjson.getObjectives() )
    values = np.empty( (0, length), float)
    
    # 2. Collect all coordinates
    for i in range(1, 20):
        # 2a. Read in a generation file
        optjson.readGeneration(i)
    
        # 2b. Get all design variables (input)
        dvars = optjson.getAllInput()
        
        # 2c. Append rows
        coords = np.vstack( (coords, dvars) )
        
        # 2d. Get all objectives (output)
        objs = optjson.getAllOutput()
        
        # 2e. Append rows
        values = np.vstack( (values, objs) )
    
    # find duplicate, otherwise we have a singular matrix
    # which is not good for Rbf
    uni, idx = np.unique(values[:, 0], return_index=True)
    
    coords = coords[idx, :]
    values = values[idx, :]
    
    shape = np.shape(coords)
    print ( "#Training points: " + str( shape[0] ) )
    print ( "#dvar:            " + str( shape[1] ) )
    
    shape = np.shape(values)
    print ( "#objs:            " + str( shape[1] ) )
    
    intpl = inpl.Interpolator()
    
    
    optjson.readGeneration(1)
    objs = optjson.getAllOutput()
    point = dvars[25, :]
    
    print ( "Evaluate at   " + str(point) )
    
    # train the interpolator
    objs_intpl = []
    for i in range(3):
        intpl.train(coords, values[:, i], function='linear', smooth=0)
        objs_intpl.append( float(intpl.evaluate(point)) )
    
    print ( "Interpolated: " + str(objs_intpl) )
    print ( "Real        : " + str(objs[25, :]) + "\n")
    
    
    
    
    point = [0.0716617, 113.828, -0.0171088, 2015.2]
    
    print ( "Evaluate at   " + str(point) )
    
    # train the interpolator
    objs_intpl = []
    for i in range(3):
        intpl.train(coords, values[:, i])
        objs_intpl.append( float(intpl.evaluate(point)) )
    
    print ( "Interpolated: " + str(objs_intpl) )
    print ( "Real        : " + str([11.97, 13.17, 8.67396]) + "\n")
    
    print ( " ----------------------------------\n" +
            "      LinearNDInterpolator\n" +
            " ----------------------------------\n")
    
    lin = LinearNDInterpolator(coords, values, fill_value=0.0, rescale=True)
    
    
    #
    #   Test at individual of same generation
    #
    
    #{
        #"ID": 25,
            #"obj":
            #{
                    #"dpeak1": 86.35,
                    #"dpeak2": 104.15,
                    #"dpeak3_5": 38.2592
            #}
            #,
            #"dvar":
            #{
                    #"benergy": 0.0713963,
                    #"phiinit": 106.037,
                    #"prinit": -0.0147301,
                    #"rinit": 2034.71
            #}
    #}
    
    point = dvars[25, :]
    
    print ( "Evaluate at   " + str(point) )
    
    print ( "Interpolated: " + str(lin(point)) )
    print ( "Real        : " + str(objs[25, :]) + "\n")
    
    
    #
    # Test at individual at another generation
    #
    
    #{
            #"ID": 79,
            #"obj":
            #{
                    #"dpeak1": 11.97,
                    #"dpeak2": 13.17,
                    #"dpeak3_5": 8.67396
            #}
            #,
            #"dvar":
            #{
                    #"benergy": 0.0716617,
                    #"phiinit": 113.828,
                    #"prinit": -0.0171088,
                    #"rinit": 2015.2
            #}
    #}
    
    point = [0.0716617, 113.828, -0.0171088, 2015.2]
    
    print ( "Evaluate at   " + str(point) )
    
    print ( "Interpolated: " + str(lin(point)) )
    print ( "Real        : " + str([11.97, 13.17, 8.67396]) )

except:
    print ( sys.exc_info()[1] )