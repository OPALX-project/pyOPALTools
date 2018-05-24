from opal.visualization.optimizer.helper import sort_list
import opal.config as config
from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
import matplotlib.pyplot as plt
import numpy as np

def plot_parallel_coordinates(ds, gen, **kwargs):
    try:
        import plotly.plotly as py
        import plotly.graph_objs as go
    
        if config.opal['style'] == 'jupyter':
            from plotly.offline import iplot as pyplot
        else:
            from plotly.offline import plot as pyplot
    except:
        print ( "Install plotly: pip install plotly" )
    
    
    """
    Plotting function for multiobjective
    optimizer output.
    
    Parameters
    ----------
    ds          (OptimizerDataset)  optimizer output dataset
    gen         (int)               generation to plot
    
    Returns
    -------
    None
    
    
    References (30. April 2018)
    ----------
    https://plot.ly/python/static-image-export/
    https://plot.ly/python/parallel-coordinates-plot/
    https://stackoverflow.com/questions/40243446/how-to-save-plotly-offline-graph-in-format-png
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.OPTIMIZER:
        raise TypeError(ds.filename + ' is not an optimizer dataset.')
    
    basename = ds.getGenerationBasename(gen)
    
    dvar_names  = ds.design_variables
    dvar_bounds = ds.bounds
    obj_names   = ds.objectives
    ids = ds.individuals(gen)
    
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
    
    for i in ids:
        data = ds.getData('', gen=gen, ind=i)
        
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
        title = 'Generation ' + str(gen)
    )
    
    fig = go.Figure(data = data, layout = layout)
    
    pyplot(fig,
           #image='png',
           #image_filename=filename,
           #output_type='file',
           filename='generation_' + str(gen) + '.html')
           #auto_open=False)


def plot_objectives(ds, **kwargs):
    """
    Plotting function for multiobjective
    optimizer output. Show the trend of
    the sum of the objectives with the generation.
    
    Parameters
    ----------
    ds          (OptimizerDataset)  optimizer output dataset
    
    Optionals
    ---------
    xscale      (str)   'linear' or 'log',
                        default: linear
    yscale      (str)   'linear' or 'log',
                        default: linear
    grid        (bool)  show grid, default: False
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.OPTIMIZER:
        raise TypeError(ds.filename + ' is not an optimizer dataset.')
    
    
    gens = range(1, ds.num_generations + 1)
    objs = ds.objectives
    
    result = []
    for g in gens:
        s = 0.0
        for obj in objs:
            s += sum(ds.getData(obj, gen=g))
        result.append( s )
    
    plt.plot(gens, result)
    plt.xscale(kwargs.get('xscale', 'linear'))
    plt.yscale(kwargs.get('yscale', 'linear'))
    plt.grid(kwargs.get('grid', True), which='both')
    plt.xlabel('generation')
    plt.ylabel('sum of objectives (all individuals)')
    
    return plt
