from .BasePlotter import *
import numpy as np
import matplotlib.gridspec as gridspec
import bisect
from opal import config as config
import re

class OptimizerPlotter(BasePlotter):
    
    def __init__(self):
        pass
    

    # 2. Mai 2018
    # https://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort
    def __natural_sort(self, l): 
        convert = lambda text: int(text) if text.isdigit() else text.lower() 
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        return sorted(l, key = alphanum_key)


    # 2. Mai 2018
    # https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    def __find(self, lst, key, value):
        for i, dic in enumerate(lst):
            if dic[key] == value:
                return i
        return None


    def __sort_list(self, names, dimension, key):
        natsort_names = self.__natural_sort(names)
        natsort_dimension = []
        for name in natsort_names:
            idx = self.__find(dimension, 'label', name)
            natsort_dimension.append(dimension[idx])
        return natsort_dimension
    
    
    def plot_parallel_coordinates(self, gen, opt=0, **kwargs):
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
        gen         (int)               generation to plot
        opt         (int)               optimizer number (default: 0)
        
        Returns
        -------
        None
        
        
        References (30. April 2018)
        ----------
        https://plot.ly/python/static-image-export/
        https://plot.ly/python/parallel-coordinates-plot/
        https://stackoverflow.com/questions/40243446/how-to-save-plotly-offline-graph-in-format-png
        """
        basename = self.ds.getGenerationBasename(gen, opt)
        
        dvar_names  = self.ds.design_variables
        dvar_bounds = self.ds.bounds
        obj_names   = self.ds.objectives
        ids = self.ds.individuals(gen, opt)
        
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
            data = self.ds.getData('', gen=gen, ind=i, opt=opt)
            
            for j, d in enumerate(data):
                if j < nDvars:
                    dvar_dimension[j]['values'].append(d)
                elif j < nDvars + nObjs:
                    obj_dimension[j - nDvars]['values'].append(d)
        
        # make a natural ordering of labels
        dvar_dimension = self.__sort_list(dvar_names,
                                          dvar_dimension,
                                          'label')
        
        obj_dimension = self.__sort_list(obj_names,
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


    def plot_objectives(self, opt=0, **kwargs):
        """
        Plotting function for multiobjective
        optimizer output. Show the trend of
        the sum of the objectives with the generation.
        
        Parameters
        ----------
        opt         (int)               optimizer number (default: 0)
        
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
        gens = range(1, self.ds.num_generations + 1)
        objs = self.ds.objectives
        
        
        avg = kwargs.pop('avg', True)
        result = []
        for g in gens:
            s = 0.0
            for obj in objs:
                if avg:
                    s += np.mean(self.ds.getData(obj, gen=g, opt=opt))
                else:
                    s += sum(self.ds.getData(obj, gen=g, opt=opt))
            result.append( s )
        
        plt.plot(gens, result)
        plt.xscale(kwargs.pop('xscale', 'linear'))
        plt.yscale(kwargs.pop('yscale', 'linear'))
        plt.grid(kwargs.pop('grid', True), which='both')
        plt.xlabel('generation')
        plt.ylabel('sum of objectives (all individuals)')
        
        return plt


    def plot_objective_evolution(self, opt=0, objs=[], op=min, **kwargs):
        """
        Plot the improvement of the objectives with
        generation. The operator 'op' is executed between
        individuals per population
        
        Parameters
        ----------
        opt         (int)               optimizer number (default: 0)
        objs        ([str])             list of objectives, if not specified
                                        all are plotted
        op          (function)          operator, e.g. max, min, etc
        
        Optionals
        ---------
        xscale      (str)               'linear', 'log'
        yscale      (str)               'linear', 'log'
        grid        (bool)
        total       (bool)              show sum of objectives
        label_rep   (dict)              replace labels by
        as_bar      (bool)
        colorlist   ([str])
        """
        objectives = self.ds.objectives
        ngen = self.ds.num_generations
        
        xscale      = kwargs.pop('xscale', 'linear')
        yscale      = kwargs.pop('yscale', 'linear')
        grid        = kwargs.pop('grid', True)
        label_rep   = kwargs.pop('label_rep', {})
        t           = kwargs.pop('total', False)
        objmean     = kwargs.pop('objmean', False)
        objmeandict = kwargs.pop('objmeandict', {
            'linewidth': 2,
            'linestyle': 'dashed',
            'color':     'black',
            'label':     'objective mean'
        })
        indmean = kwargs.pop('indmean', False)
        indmeandict = kwargs.pop('indmeandict', {
            'linewidth': 2,
            'linestyle': 'dashed',
            'color':     'black',
            'label':     'individual mean'
        })

        totaldict  = kwargs.pop('totaldict', {
            'linewidth': 2,
            'linestyle': 'dashed',
            'color':     'black',
            'label':     'objective sum'
        })

        legenddict = kwargs.pop('legenddict', {
            'fontsize':       18,
            'ncol':           4,
            'labelspacing':   0.5,
            'bbox_to_anchor': (0.25,0.65 + (indmean) * 0.2, 0.5, 0.5)
        })

        as_bar    = kwargs.pop('asbar', False)
        colorlist = kwargs.pop('colorlist', [])

        if objs:
            for obj in objs:
                if not obj in objectives:
                    raise ValueError(self.ds.filename + ' does only has following objectives: '
                                    + str(objectives))
        else:
            objs = objectives

        result = np.zeros((len(objs), ngen))
        ind_mean = np.zeros(ngen)
        
        for j in range(0, ngen):
            ids = self.ds.individuals(j+1, opt=opt)
            
                # val, id
            cur = [0, -1]
            for idx in ids:
                s = 0
                for obj in objectives:
                    val = self.ds.getData(var=obj, gen=j+1, ind=idx, all=False, opt=opt)
                    s += val
                    if indmean:
                        ind_mean[j] += val
                
                if cur[1] < 0:
                    cur = [s, idx]
                else:
                    cur = op([s, idx], cur)
            
            if indmean:
                ind_mean[j] /= len(ids)

            for i, obj in enumerate(objs):
                result[i, j] = self.ds.getData(obj, gen=j+1, ind=cur[1], all=False, opt=opt)

        label = []
        for i, obj in enumerate(objs):
            label.append( obj )
            if obj in label_rep.keys():
                label[-1] = label_rep[obj]

        if indmean:
            plt.subplot(2, 1, 1)
            plt.semilogy(range(1, ngen + 1), ind_mean, **indmeandict)
            plt.xscale(xscale)
            plt.xlabel('generation')
            plt.ylabel('individual mean')
            plt.grid(grid, which='both')
            
            plt.subplot(2, 1, 2)

        if as_bar:
            # bar plot
            bottom = [0] * np.shape(result)[1]
            for i, obj in enumerate(objs):
                if i < len(colorlist) - 1:
                    kwargs['color'] = colorlist[i]
                else:
                    kwargs.pop('color', 'black')
                plt.bar(range(1, ngen + 1), result[i, :], label=label[i],
                        bottom=bottom, **kwargs)
                bottom += result[i, :]
        else:
            for i, obj in enumerate(objs):
                if i < len(colorlist) - 1:
                    kwargs['color'] = colorlist[i]
                else:
                    kwargs.pop('color', 'black')
                plt.plot(range(1, ngen + 1), result[i, :], label=label[i], **kwargs)
        
            if t:
                total = result.sum(axis=0)
                plt.plot(range(1, ngen + 1), total, **totaldict)

        if objmean:
            mean = result.mean(axis=0)
            plt.plot(range(1, ngen + 1), mean, **objmeandict)
        
        plt.xlabel('generation')
        plt.xscale(xscale)
        plt.yscale(yscale)
        plt.grid(grid, which='both')
        
        if len(objs) > 1:
            plt.ylabel(op.__name__)
            plt.legend()
        else:
            plt.ylabel(obj)
        
        plt.legend(loc = 'upper center', **legenddict)

        if indmean:
            plt.subplots_adjust(hspace = 10)

        return plt


    def plot_dvar_evolution(self, opt=0, dvars=[], op=min, **kwargs):
        """
        Plot the evolution of the design variable values
        dependent on the improvement of the objectives with
        generation. The operator 'op' is executed on two
        objective value sums of two individuals.
        
        Parameters
        ----------
        opt         (int)               optimizer number (default: 0)
        dvars       ([str])             list of design variables, if not specified
                                        all are plotted
        op          (function)          operator, e.g. max, min, etc
        
        Optionals
        ---------
        xscale      (str)               'linear', 'log'
        yscale      (str)               'linear', 'log'
        grid        (bool)
        """
        objs = self.ds.objectives
        ngen = self.ds.num_generations
        dvs  = self.ds.design_variables
        
        if dvars:
            for dvar in dvars:
                if not dvar in dvs:
                    raise ValueError(self.ds.filename + ' does only has following design variables: '
                                    + str(dvs))
        else:
            dvars = dvs
        
        result = np.zeros((len(dvars), ngen))
        
        for j in range(0, ngen):
            ids = self.ds.individuals(j+1, opt=opt)
            
                # val, id
            cur = [0, -1]
            for idx in ids:
                s = 0
                for obj in objs:
                    s += self.ds.getData(var=obj, gen=j+1, ind=idx, all=False, opt=opt)
                
                if cur[1] < 0:
                    cur = [s, idx]
                else:
                    cur = op([s, idx], cur)
            
            for i, dvar in enumerate(dvars):
                result[i, j] = self.ds.getData(dvar, gen=j+1, ind=cur[1], all=False, opt=opt)
        
        for i, dvar in enumerate(dvars):
            plt.plot(range(1, ngen + 1), result[i, :], label=dvar)
        
        plt.xlabel('generation')
        plt.xscale(kwargs.pop('xscale', 'linear'))
        plt.yscale(kwargs.pop('yscale', 'linear'))
        plt.grid(kwargs.pop('grid', True), which='both')
        
        if len(dvars) > 1:
            plt.ylabel(op.__name__)
            plt.legend()
        else:
            plt.ylabel(dvar)
        
        return plt


    def plot_pareto_front(self, xdvar, ydvar, opt=0, **kwargs):
        """
        Plot the Pareto front

        Parameters
        ----------
        xdvar       (str)               design variable on x-axis
        ydvar       (str)               design variable on y-axis
        opt         (int)               optimizer number (default: 0)

        Returns
        -------
        a matplotlib.pyplot handle
        """
        x = self.ds.getData(var=xdvar, opt=opt, pareto=True)
        y = self.ds.getData(var=ydvar, opt=opt, pareto=True)

        ind = np.argsort(x)
        plt.scatter(x[ind], y[ind], **kwargs)
        plt.xlabel(self.ds.getLabel(xdvar))
        plt.ylabel(self.ds.getLabel(ydvar))

        return plt


    def plot_individual_bounds(self, n, opt=0, **kwargs):
        """
        Plot all design variables and their bounds. This
        will show if a design variable is close to one
        of its bounds.
        
        Parameters
        ----------
        opt         (int)               optimizer number (default: 0)
        n           (int)               take the first n-th best individuals
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        # 02. Nov. 2018
        # https://stackoverflow.com/questions/8024571/insert-an-item-into-sorted-list-in-python
        
        objs = self.ds.objectives
        
        ids = self.ds.individuals(1, opt=opt)
        
        # restrict
        if n < 1:
            n = 1
        if n > len(ids):
            n = len(ids)
        
        nbests = []
        values = []
        for gen in range(1, self.ds.num_generations + 1):
            ids = self.ds.individuals(gen, opt=opt)
            
            for ind in ids:
                s = 0.0
                for obj in objs:
                    s += self.ds.getData(var=obj, gen=gen, ind=ind, all=False, opt=opt)
                # [sum, generation, individual id]
                
                if s not in values:
                    bisect.insort(nbests, [gen, ind])
                    bisect.insort(values, s)
                
                if len(nbests) > n:
                    del nbests[-1]
                    del values[-1]
        
        dvars = self.ds.design_variables
        
        if not dvars:
            raise IndexError('No design variables found.')
        
        ncols = kwargs.pop('ncols', 4)
        nrows = int(np.ceil(len(dvars) / ncols + 0.5))
        
        gs = gridspec.GridSpec(nrows, ncols)
        
        # each row is an individual
        # each col is a design variable value
        data = np.zeros([n, len(dvars)])
        
        for i, best in enumerate(nbests):
            # each list index has a dictionary
            # that contains just 1 entry, i.e. a list of 2 values (gen, ind)
            gen, ind = best
            
            for j, dvar in enumerate(dvars):
                data[i][j] = self.ds.getData(var=dvar, gen=gen, ind=ind, all=False, opt=opt)
        
        bnds = self.ds.bounds
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
