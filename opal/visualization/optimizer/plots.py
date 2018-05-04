from opal.visualization.optimizer.helper import sort_list
import opal.config as config

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
        data = ds.getData(i)
        
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
