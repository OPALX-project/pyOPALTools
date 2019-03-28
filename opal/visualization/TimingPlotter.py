# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.visualization.BasePlotter import *
import numpy as np
from operator import itemgetter

class TimingPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    
    def __mostConsuming(self, n, times, labels, prop):
        """
        Retturn time and label of the first n most time
        consuming timings.
        
        Parameters
        ----------
        n       (int)   number of timings
        times   ([])    list of timing data
        labels  ([])    list of labels to appropriate timings
        
        Returns
        -------
        sorted times and labels
        """
        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/9543211/sorting-a-list-in-python-using-the-result-from-sorting-another-list
        times_sorted, labels_sorted = zip(*sorted(zip(times, labels),
                                                key=itemgetter(0),
                                                reverse=True))
        
        if n < 0:
            n = 1
        elif n > len(times_sorted):
            n = len(times_sorted)
        
        return list(times_sorted[0:n]), list(labels_sorted[0:n])


    def plot_efficiency(self, dsets, what, prop, **kwargs):
        """
        Efficiency plot of a timing benchmark study
        
        E_p = S_p / p
        
        where E_p is the efficiency and S_p the
        speed-up with p cores / nodes.
        
        Parameters
        ----------
        dsets   ([TimeDataset]) all timing datasets
        what    (str)           timing name
        prop    (str)           property, i.e. 'cpu avg', 'cpu max', 'cpu min',
                                'wall avg', 'wall max', 'wall min' or
                                'cpu tot' and 'wall tot' (only for main timing)
        
        Optionals
        ---------
        xscale      (str)           x-axis scale, 'linear' or 'log'
        yscale      (str)           y-axis scale, 'linear' or 'log'
        grid        (bool)          if true, plot grid
        percent     (bool)          efficiency in percentage
        xlabel      (str)           label for x-axis. Default '#cores'
        core2node   (int)           scale #cores == 1 node
                                    (useful with xlabel='#nodes')
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if not isinstance(dsets, list):
            dsets = [dsets]
        
        dsets = [seld.ds] + dsets
        
        for ds in dsets:
            if not ds.filetype == FileType.TIMING and not ds.filetype == FileType.OUTPUT:
                raise TypeError("Dataset '" + ds.filename +
                                "' is not a timing dataset.")
        
        cores = []
        time = []
        
        for ds in dsets:
            #access main timing
            cores.append( int(ds.getData(0, prop='cores')) )
            
            time.append( ds.getData(var=what, prop=prop) )
        
        # sort
        cores, time = zip(*sorted(zip(cores, time)))
        
        # tuple --> list
        cores = list(cores)
        
        # transform cores --> nodes
        core2node = kwargs.pop('core2node', 1)
        
        for i, c in enumerate(cores):
            cores[i] /= core2node
        
        
        # obtain speed-up
        speedup = []
        for t in time:
            speedup.append( time[0] / t )
        
        # obtain core increase
        incr = []
        for c in cores:
            incr.append( c / cores[0] )   
        
        # obtain efficiency
        efficiency = []
        
        percent = 1.0
        ylabel  = 'efficiency'
        if kwargs.pop('percent', True):
            percent = 100.0
            ylabel += ' [%]'
        
        for i, s in enumerate(speedup):
            efficiency.append( s / incr[i] * percent ) # in percent
        
        xscale = kwargs.pop('xscale', 'linear')
        yscale = kwargs.pop('yscale', 'linear')
        grid   = kwargs.pop('grid', False)
        
        plt.plot(cores, efficiency)
        plt.xlabel(kwargs.pop('xlabel', '#cores'))
        plt.ylabel(ylabel)
        plt.xscale(xscale)
        plt.yscale(yscale)
        plt.grid(grid, which='both')
        plt.tight_layout()
        
        return plt


    def plot_speedup(self, dsets, what, prop, **kwargs):
        """
        Speedup plot of a timing benchmark study
        
        S_p = T_1 / T_p
        
        where T_1 is the time for a single core run
        (or reference run with several cores / nodes)
        and T_p the time with p cores. S_p then represents the
        speed-up with p cores / nodes.
        
        Parameters
        ----------
        dsets   ([TimeDataset]) all timing datasets
        what    (str)           timing name
        prop    (str)           property, i.e. 'cpu avg', 'cpu max', 'cpu min',
                                'wall avg', 'wall max', 'wall min' or
                                'cpu tot' and 'wall tot' (only for main timing)
        
        Optionals
        ---------
        xscale          (str)           x-axis scale, 'linear' or 'log'
        yscale          (str)           y-axis scale, 'linear' or 'log'
        grid            (bool)          if true, plot grid
        efficiency      (bool)          add efficiency to plot
        xlabel          (str)           label for x-axis. Default '#cores'
        core2node       (int)           scale #cores == 1 node
                                        (useful with xlabel='#nodes')
        perfect_scaling (bool)          add speed-up perfect scaling line
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if not isinstance(dsets, list):
            dsets = [dsets]
        
        dsets = [self.ds] + dsets
        
        for ds in dsets:
            if not ds.filetype == FileType.TIMING and not ds.filetype == FileType.OUTPUT:
                raise TypeError("Dataset '" + ds.filename +
                                "' is not a timing dataset.")
        
        cores = []
        time = []
        
        for ds in dsets:
            #access main timing
            cores.append( int(ds.getData(0, prop='cores')) )
            
            time.append( ds.getData(var=what, prop=prop) )
        
        # sort
        cores, time = zip(*sorted(zip(cores, time)))
        
        # tuple --> list
        cores = list(cores)
        
        # transform cores --> nodes
        core2node = kwargs.pop('core2node', 1)
        
        for i, c in enumerate(cores):
            cores[i] /= core2node
        
        # obtain speed-up
        speedup = []
        for t in time:
            speedup.append( time[0] / t )
        
        xscale = kwargs.pop('xscale', 'linear')
        yscale = kwargs.pop('yscale', 'linear')
        grid   = kwargs.pop('grid', False)
        
        ax1 = plt.gca()
        loc = 'best'
        
        if kwargs.pop('efficiency', False):
            loc = 'lower center'
            
            # obtain core increase
            incr = []
            for c in cores:
                incr.append( c / cores[0] )   
            
            # obtain efficiency
            efficiency = []
            
            ax2 = ax1.twinx()
            ax2.set_ylabel('efficiency', color='r')
            ax2.set_yscale(yscale)
            # 8. April 2018
            # https://stackoverflow.com/questions/15256660/set-the-colour-of-matplotlib-ticks-on-a-log-scaled-axes
            ax2.tick_params('y', colors='r', which='both')
            ax2.grid(grid, which='both', color='r', linestyle='dashed', alpha=0.4)
            
            for i, s in enumerate(speedup):
                efficiency.append( s / incr[i] )
            
            ax2.plot(cores, efficiency, 'r')
        
        ax1.plot(cores, speedup, label=ds.getLabel(what))
        ax1.set_xlabel(kwargs.pop('xlabel', '#cores'))
        ax1.set_ylabel('speed-up')
        ax1.set_xscale(xscale)
        ax1.set_yscale(yscale)
        ax1.grid(grid, which='both')
        
        if kwargs.pop('perfect_scaling', False):
            ref = []
            for c in cores:
                ref.append( c / cores[0] )
            ax1.plot(cores, ref, 'k--', label='perfect scaling')
            ax1.legend(frameon=True, loc=loc)
        
        plt.tight_layout()
            
        return plt


    def plot_time_scaling(self, dsets, prop, **kwargs):
        """
        Plot timing benchmark.
        
        Parameters
        ----------
        dsets   ([TimeDataset]) all timing datasets
        prop    (str)           property, 'wall' or 'cpu
        
        Optionals
        ---------
        first=None      (int)   take only the first N specialized
        xscale          (str)           x-axis scale, 'linear' or 'log'
        yscale          (str)           y-axis scale, 'linear' or 'log'
        grid            (bool)          if true, plot grid
        xlabel          (str)           label for x-axis. Default '#cores'
        core2node       (int)           scale #cores == 1 node
                                        (useful with xlabel='#nodes')
        exclude         ([])            do not use *these* timings
        tag=''          (str)           take only timings containing this tag
        perfect_scaling (bool)          add speed-up perfect scaling line
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if not isinstance(dsets, list):
            dsets = [dsets]
        
        dsets = [seld.ds] + dsets
        
        for ds in dsets:
            if not ds.filetype == FileType.TIMING and not ds.filetype == FileType.OUTPUT:
                raise TypeError("Dataset '" + ds.filename +
                                "' is not a timing dataset.")
        
        if not prop == 'wall' and not prop == 'cpu':
            raise ValueError("Wrong property value: prop = 'wall' or prop = 'cpu'.")
        
        cores = []
        for ds in dsets:
            cores.append( int(ds.getData(0, prop='cores')) )
        
        # sort
        cores, dsets = zip(*sorted(zip(cores, dsets)))
        
        # tuple --> list
        cores = list(cores)
        
        # transform cores --> nodes
        core2node = kwargs.pop('core2node', 1)
        
        for i, c in enumerate(cores):
            cores[i] /= core2node
        
        labels = []
        times  = []
        excludeList = kwargs.pop('exclude', [])
        tag         = kwargs.pop('tag', '')
        
        for name in dsets[0].getLabels():
            skip = False
            for ex in excludeList:
                if ex in name:
                    skip = True
                    break
            if not skip and not 'main' in name and tag in name:
                labels.append( name )
                times.append( dsets[0].getData(var=name, prop=prop + ' avg') )
        
        times, labels = self.__mostConsuming(kwargs.pop('first', 1e6), times, labels, prop + ' avg')
        
        times, labels = zip(*sorted(zip(times, labels),
                                key=itemgetter(0),
                                reverse=True))
        
        for label in labels:
            tmin = []
            tmax = []
            tavg = []
            for ds in dsets:
                tavg.append( ds.getData(var=label, prop=prop + ' avg') )
                tmin.append( tavg[-1] - ds.getData(var=label, prop=prop + ' min') )
                tmax.append( ds.getData(var=label, prop=prop + ' max') - tavg[-1] )
            
            plt.errorbar(cores, tavg, yerr=[tmin, tmax], fmt='--o', label=label)
        
        plt.grid(kwargs.pop('grid', False), which="both")
        plt.xlabel(kwargs.pop('xlabel', '#cores'))
        plt.ylabel('time [' + ds.getUnit('') + ']')
        plt.xlim([0.5*cores[0], 1.05*cores[-1]])
        plt.xscale(kwargs.pop('xscale', 'linear'))
        plt.yscale(kwargs.pop('yscale', 'linear'))
        plt.tight_layout()
        
        
        if kwargs.pop('perfect_scaling', False):
            ref = []
            for c in cores:
                ref.append( times[0] * cores[0] / c )
            plt.plot(cores, ref, 'k', label='perfect scaling')
        plt.legend(loc='best')
        
        return plt


    def plot_time_summary(self, prop, **kwargs):
        """
        Create a plot with minimum, maximum and average timings
        
        Parameters
        ----------
        ds      (DatasetBase)   timing dataset
        prop    (str)           property, 'wall' or 'cpu
        
        Optionals
        ---------
        yscale          (str)           y-axis scale, 'linear' or 'log'
        grid            (bool)          if true, plot grid
        exclude         ([])            do not use *these* timings
        tag=''          (str)           take only timings containing this tag
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        if not prop == 'wall' and not prop == 'cpu':
            raise ValueError("Wrong property value: prop = 'wall' or prop = 'cpu'.")
        
        labels = []
        excludeList = kwargs.pop('exclude', [])
        tag         = kwargs.pop('tag', '')
        for name in self.ds.getLabels():
            skip = False
            for ex in excludeList:
                if ex in name:
                    skip = True
                    break
            if not skip and not 'main' in name and tag in name:
                labels.append( name )
        
        tmin = []
        tmax = []
        tavg = []
        
        for name in labels:
            tavg.append( self.ds.getData(var=name, prop=prop + ' avg') )
            tmin.append( tavg[-1] - self.ds.getData(var=name, prop=prop + ' min') )
            tmax.append( self.ds.getData(var=name, prop=prop + ' max') - tavg[-1] )
        
        n = len(tavg)
        x = np.linspace(0, n-1, n)

        grid   = kwargs.pop('grid', False)
        yscale = kwargs.pop('yscale', 'linear')
        plt.errorbar(x, tavg, yerr=[tmin, tmax], fmt='o', **kwargs)
        plt.xlim([-1, n])
        plt.ylim([-10, max(tmax)+max(tavg)])
        plt.ylabel('time [' + self.ds.getUnit('') + ']')
        # 2. Feb. 2018
        # https://stackoverflow.com/questions/14852821/aligning-rotated-xticklabels-with-their-respective-xticks
        plt.xticks(x, labels, rotation=45, ha='right')
        plt.grid(grid, which="both")

        ax = plt.gca()
        if yscale == 'log':
            ax.set_yscale('log', nonposy='clip')

        plt.tight_layout()
        
        return plt


    def plot_pie_chart(self, prop, **kwargs):
        """
        Create a pie plot of the first N most time consuming timings.
        
        Parameters
        ----------
        ds      (DatasetBase)   timing dataset
        prop    (str)           property, i.e. 'cpu avg', 'cpu max', 'cpu min',
                                'wall avg', 'wall max', 'wall min' or
                                'cpu tot' and 'wall tot' (only for main timing)
        
        Optionals
        ---------
        first=None          (int)   take only the first N specialized
                                    timings
        exclude             ([])    do not use *these* timings
        tag=''              (str)   what tag should be in name
        cmap_name='YlGn'    (str)   color scheme
        
        Notes
        -----
        Throws an exception if file not available or the key is not part
        of the dictionary
        
        Returns
        -------
        a matplotlib.pyplot handle
        """
        first = kwargs.pop('first', None)
        cmap_name = kwargs.pop('cmap', 'YlGn')
        
        names = self.ds.getLabels()
        
        labels = []
        times  = []
        for name in names:
            if not 'main' in name:
                labels.append(name)
                times.append( self.ds.getData(var=name, prop=prop) )
        
        times_sorted, labels_sorted = self.__mostConsuming(first, times, labels, prop)
        
        # sum up all others
        if first:
            labels_sorted.append('others')
            t = 0.0
            for name in names:
                if not 'main' in name and name not in labels_sorted:
                    t += self.ds.getData(var=name, prop=prop)
            times_sorted.append(t)
        
        times_sorted, labels_sorted = zip(*sorted(zip(times_sorted, labels_sorted),
                                                key=itemgetter(0),
                                                reverse=True))
        
        # 15. Jan. 2017, https://gist.github.com/vals/5257113
        cmap = plt.get_cmap(cmap_name)
        colors = cmap(np.linspace(0, 1, len(times_sorted)))
            
        explode = [0.0] * len(times_sorted)

        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/7082345/how-to-set-the-labels-size-on-a-pie-chart-in-python
        patches, texts, autotexts = plt.pie(times_sorted,
                                            autopct='%1.1f%%',
                                            pctdistance=0.7,
                                            labeldistance=1.0,
                                            startangle=90,
                                            explode=explode,
                                            colors=colors,
                                            radius=1.1,
                                            shadow=False)
        
        for at in autotexts:
            at.set_fontsize(10)
        
        plt.legend(patches, labels_sorted, loc='best', bbox_to_anchor=(0.95, 0.98), borderaxespad=0.1)
        plt.axis('equal')
        
        return plt
