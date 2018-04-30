from visualize_pf import readData, nameToColumnMap
import argparse, os, sys, glob

import OptPilotJsonReader as jsonreader

try:
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly.offline import plot
except:
    print ( "Install plotly: pip install plotly" )


def plot_parcoords(path, filename_postfix, filename):
    """
    
    References (30. April 2018)
    ----------
    https://plot.ly/python/static-image-export/
    https://plot.ly/python/parallel-coordinates-plot/
    https://stackoverflow.com/questions/40243446/how-to-save-plotly-offline-graph-in-format-png
    """
    
    first = True
    
    values = {}
    
    min_error = 1e8
    max_error = -1e-8
    
    
    for infile in glob.glob(os.path.join(path,
                            '*_' + filename_postfix)):
        
        dirname = os.path.dirname(infile)
        optjson = jsonreader.OptPilotJsonReader(dirname + '/')
        
        # get the generation from the filename
        basename = os.path.basename(infile)    
        
        generation = int( str.split(basename, "_", 1)[0] )
        optjson.readGeneration(generation)
        
        if first:
            first = False
            
            
            dvar_names  = optjson.getDesignVariables()
            dvar_bounds = optjson.getBounds()
            obj_names   = optjson.getObjectives()
            
            dimension = []
            
            for dvar in dvar_names:
                dimension.append({
                    'range': dvar_bounds[dvar],
                    'label': dvar,
                    'values': []
                    }
                )
                
                values[dvar] = []
            
            for obj in obj_names:
                dimension.append({
                    'label': obj,
                    'values': []
                    }
                )
                
                values[obj] = []
        
        for i in optjson.getIDs():
            data = optjson.getIndividualWithID(i)
            
            j = 0
            
            for d in data:
                
                if j < len(dvar_names):
                    values[dvar_names[j]].append(d)
                elif j < len(dvar_names) + len(obj_names):
                    values[obj_names[j - len(dvar_names)]].append(d)
                    
                    min_error = min(min_error, d)
                    max_error = max(max_error, d)
                    
                j += 1
    
    
    
    ids = optjson.getIDs()
    
    
    for i, dvar in enumerate(dvar_names):
        dimension[i]['values'] = values[dvar]
    
    for i, obj in enumerate(obj_names):
        dimension[i + len(dvar_names)]['values'] = values[obj]
    
    
    data = [
        go.Parcoords(
            line = dict(color = ids,
                        colorscale = 'Jet',
                        showscale = True,
                        reversescale = True,
                        cmin = min_error,
                        cmax = max_error),
            dimensions = dimension
        )
    ]
    
    
    plot(data,
         image='png',
         image_filename=filename,
         output_type='file')
         #auto_open=False)


if __name__ == "__main__":
    path = ""
    outpath = "./"
    filename_postfix = "results.json"
    
    try:
        ## Parse input arguments
        parser = argparse.ArgumentParser()
        
        parser.add_argument("-p",
                            "--path",
                            dest="path",
                            type=str,
                            default=path,
                            help="specify the path of the result files")
    
        parser.add_argument("-f",
                            "--filename-postfix",
                            dest="filename_postfix",
                            type=str,
                            default=filename_postfix,
                            help="(default: 'results.json'): specify a custom file postfix of result files")
        
        parser.add_argument("-u",
                            "--outpath",
                            dest="outpath",
                            type=str,
                            default=outpath,
                            help="path for storing resulting pngs")
        
        args = parser.parse_args()
        
        
        path             = args.path
        filename_postfix = args.filename_postfix
        outpath          = args.outpath
        
        if path == "":
            raise SyntaxError('No path for input data specified')
    
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        
        plot_parcoords(path, filename_postfix, 'parcoords-advanced')
        
    except:
        print ( '\n\t\033[01;31mError: ' + str(sys.exc_info()[1]) + '\n' )
