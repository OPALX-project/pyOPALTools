from visualize_pf import readData, nameToColumnMap
import argparse, os, sys, glob
import re


from opal.parser.OptimizerParser import OptimizerParser as jsonreader

try:
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly.offline import plot
except:
    print ( "Install plotly: pip install plotly" )
    

# 2. Mai 2018
# https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


# 2. Mai 2018
# https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return None


def sort_list(names, dimension, key):
    natsort_names = natural_sort(names)
    natsort_dimension = []
    for name in natsort_names:
        idx = find(dimension, 'label', name)
        natsort_dimension.append(dimension[idx])
    return natsort_dimension


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
    optjson = jsonreader(dirname + '/')
        
    # get the generation from the filename
    basename = os.path.basename(infile)    
        
    generation = int( str.split(basename, "_", 1)[0] )
    optjson.readGeneration(generation)
        
    dvar_names  = optjson.getDesignVariables()
    dvar_bounds = optjson.getBounds()
    obj_names   = optjson.getObjectives()
            
    dvar_dimension = []
    obj_dimension = []
    
    for dvar in dvar_names:
        dvar_dimension.append({
            'range': dvar_bounds[dvar],
            'label': dvar,
            'values': []
            }
        )
    
    for obj in obj_names:
        obj_dimension.append({
            'label': obj,
            'values': []
            }
        )
    
    nDvars = len(dvar_names)
    nObjs = len(obj_names)
    for i in optjson.getIDs():
        data = optjson.getIndividualWithID(i)
        
        for j, d in enumerate(data):
            if j < nDvars:
                dvar_dimension[j]['values'].append(d)
            elif j < nDvars + nObjs:
                obj_dimension[j - nDvars]['values'].append(d)
    
    # make a natural ordering of labels
    dvar_dimension = sort_list(dvar_names,
                               dvar_dimension,
                               'label')
    
    obj_dimension = sort_list(obj_names,
                              obj_dimension,
                              'label')
    
    dimension = dvar_dimension + obj_dimension
    
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
