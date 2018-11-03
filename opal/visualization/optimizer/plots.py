from opal.visualization.optimizer.helper import sort_list
import opal.config as config
from opal.datasets.filetype import FileType
from opal.datasets.DatasetBase import DatasetBase
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import bisect

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
        height=800,
        width=1600,
        font=dict(size=18),
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
    avg         (bool)  take averaged sum over all objectives
                        default: true
    
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
    
    
    avg = kwargs.pop('avg', True)
    result = []
    for g in gens:
        s = 0.0
        for obj in objs:
            if avg:
                s += np.mean(ds.getData(obj, gen=g))
            else:
                s += sum(ds.getData(obj, gen=g))
        result.append( s )
    
    plt.plot(gens, result)
    plt.xscale(kwargs.get('xscale', 'linear'))
    plt.yscale(kwargs.get('yscale', 'linear'))
    plt.grid(kwargs.get('grid', True), which='both')
    plt.xlabel('generation')
    plt.ylabel('sum of objectives (all individuals)')
    
    return plt


def plot_individual_bounds(ds, n, **kwargs):
    """
    Plot all design variables and their bounds. This
    will show if a design variable is close to one
    of its bounds.
    
    Parameters
    ----------
    ds          (OptimizerDataset)  optimizer output dataset
    n           (int)               take the first n-th best individuals
    
    Returns
    -------
    a matplotlib.pyplot handle
    """
    if not isinstance(ds, DatasetBase):
        raise TypeError("Dataset '" + ds.filename +
                        "' not derived from 'DatasetBase'.")
    
    if not ds.filetype == FileType.OPTIMIZER:
        raise TypeError(ds.filename + ' is not an optimizer dataset.')
    
    
    # 02. Nov. 2018
    # https://stackoverflow.com/questions/8024571/insert-an-item-into-sorted-list-in-python
    
    objs = ds.objectives
    
    ids = ds.individuals(1)
    
    # restrict
    if n < 1:
        n = 1
    if n > len(ids):
        n = len(ids)
    
    nbests = []
    values = []
    for gen in range(1, ds.num_generations + 1):
        ids = ds.individuals(gen)
        
        for ind in ids:
            s = 0.0
            for obj in objs:
                s += ds.getData(var=obj, gen=gen, ind=ind, all=False)
            # [sum, generation, individual id]
            
            if s not in values:
                bisect.insort(nbests, [gen, ind])
                bisect.insort(values, s)
            
            if len(nbests) > n:
                del nbests[-1]
                del values[-1]
    
    dvars = ds.design_variables
    
    if not dvars:
        raise IndexError('No design variables found.')
    
    nrows = int(np.sqrt(len(dvars)))
    ncols = int(len(dvars) / nrows + 0.5)
    
    gs = gridspec.GridSpec(nrows, ncols)
    
    # each row is an individual
    # each col is a design variable value
    data = np.zeros([n, len(dvars)])
    
    for i, best in enumerate(nbests):
        # each list index has a dictionary
        # that contains just 1 entry, i.e. a list of 2 values (gen, ind)
        gen, ind = best
        
        for j, dvar in enumerate(dvars):
            data[i][j] = ds.getData(var=dvar, gen=gen, ind=ind, all=False)
    
    bnds = ds.bounds
    axes = []
    
    xticks = np.linspace(1, n, num=n)
    xtickstep = kwargs.pop('xtickstep', 1)
    for i, dvar in enumerate(dvars):
        ax = plt.subplot(gs[i])
        axes.append( ax )
        
        sc = ax.scatter(xticks, data[:, i], c=values, marker='o')
        ax.set_xlabel('n-th best individual')
        ax.set_ylabel(dvar)
        ax.set_xticks(np.arange(1, n+1, step=xtickstep))
        
        ax.axhline(y=bnds[dvar][0], linestyle='dashed', color='black')
        ax.axhline(y=bnds[dvar][1], linestyle='dashed', color='black',
                   label='design variable upper and lower bound')
        
        uplim = bnds[dvar][1] * 1.01
        lowlim = bnds[dvar][0] * 0.99
        if bnds[dvar][0] < 0:
            lowlim = bnds[dvar][0] * 1.01
        if bnds[dvar][1] < 0:
            uplim = bnds[dvar][1] * 0.99
        ax.set_ylim([lowlim, uplim])
    
    cbar = plt.colorbar(sc, ax=axes)
    cbar.set_label('sum of objective values')
    # 3. Nov. 2018
    # https://stackoverflow.com/questions/9834452/how-do-i-make-a-single-legend-for-many-subplots-with-matplotlib
    plt.figlegend(loc = 'lower center', ncol=ncols, labelspacing=0. )
