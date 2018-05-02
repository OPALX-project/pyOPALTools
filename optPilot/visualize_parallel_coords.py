from visualize_pf import readData, nameToColumnMap
import argparse, os, sys, glob

import OptPilotJsonReader as jsonreader

try:
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly.offline import plot
except:
    print ( "Install plotly: pip install plotly" )


def plot_parcoords(path, filename_postfix, generation, filename):
    """
    
    References (30. April 2018)
    ----------
    https://plot.ly/python/static-image-export/
    https://plot.ly/python/parallel-coordinates-plot/
    https://stackoverflow.com/questions/40243446/how-to-save-plotly-offline-graph-in-format-png
    """
    
    infile = os.path.join(path, str(generation) + '_' + filename_postfix)
        
    dirname = os.path.dirname(infile)
    optjson = jsonreader.OptPilotJsonReader(dirname + '/')
        
    # get the generation from the filename
    basename = os.path.basename(infile)    
        
    generation = int( str.split(basename, "_", 1)[0] )
    optjson.readGeneration(generation)
        
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
                
    for obj in obj_names:
        dimension.append({
            'label': obj,
            'values': []
            }
        )
                
    for i in optjson.getIDs():
        data = optjson.getIndividualWithID(i)
        
        for j, d in enumerate(data):
            if j < len(data) - 1: # skip ID
                dimension[j]['values'].append(d)
    
    ids = optjson.getIDs()
    
    data = [
        go.Parcoords(
            line = dict(color = ids,
                        colorscale = 'Jet',
                        showscale = True,
                        reversescale = True,
                        cmin = min(ids),
                        cmax = max(ids)),
            dimensions = dimension
        )
    ]
    
    layout = go.Layout(
        title = 'Generation ' + str(generation)
    )
    
    fig = go.Figure(data = data, layout = layout)
    
    plot(fig,
         #image='png',
         #image_filename=filename,
         #output_type='file',
         filename='generation_' + str(generation) + '.html')
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
        
        parser.add_argument("-g",
                            "--generation",
                            dest="generation",
                            type=int,
                            default=1,
                            help="only displays the 'n'-th generation")
        
        
        
        args             = parser.parse_args()
        generation       = args.generation
        path             = args.path
        filename_postfix = args.filename_postfix
        outpath          = args.outpath
        
        if generation < 0:
            raise ValueError("Generation number cannot be negative.")
        
        if path == "":
            raise SyntaxError('No path for input data specified')
    
        if not os.path.isdir(outpath):
            os.mkdir(outpath)
        
        plot_parcoords(path, filename_postfix, generation, 'generation_' + str(generation))
        
    except:
        print ( '\n\t\033[01;31mError: ' + str(sys.exc_info()[1]) + '\n' )
