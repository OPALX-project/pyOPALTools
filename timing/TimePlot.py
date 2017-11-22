import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import os

import timing.Timing as timing

class TimePlot:
    
    def line_plot(self, fnames, **kwargs):
        """
        Create a plot of several timings containing same timers.
        Plot the first N most time consuming timings. Timing files
        do not need to be ordered according to the number of cores.
        
        Parameters
        ----------
        fnames              (str)  timing files
        saveas              (str)   export the summary plot
        figsize=(12, 9)             size of the figure
        grid=False          (bool)  show grid
        
        Notes
        -----
        Throws an exception if a file does not exist.
        
        Returns
        -------
        None
        """
        
        # get kwargs arguments
        first = kwargs.get('first', None)
        saveas = kwargs.get('saveas', None)
        figsize = kwargs.get('figsize', (12, 9))
        grid = kwargs.get('grid', False)
        
        # check if all files exist
        cores = []
        for fname in fnames:
            if not os.path.isfile(fname):
                raise RuntimeError("The file " + "'" + fname + "'" + " does not exist.")
            
            # sort file first (inefficient) according to cores
            time = timing()
            time.read_ippl_timing(fname)
            cores.append(int(time.getTiming()[0]['cores']))
        
        cores_sorted, fnames_sorted = zip(*sorted(zip(cores, fnames),
                                                      key=itemgetter(0),
                                                      reverse=False))
        
        # read first entry
        time = timing()
        time.read_ippl_timing(fnames_sorted[0])
        data = time.getTiming()
        
        # get first n most time consuming timing labels
        times_sorted , labels_sorted = self.__getMostTimeConsuming(first+1, data, 'cpu max', True)
        
        
        tmin, tavg, tmax = self.__collect(data, labels_sorted)
        
        n = len(fnames_sorted)
        x = np.linspace(0, n-1, n)
        
        fdata = {}
        for i in range(len(tmin)):
            fdata[labels_sorted[i]] = []
            fdata[labels_sorted[i]] = {'min': [tmin[i]],
                                       'max': [tmax[i]],
                                       'avg': [tavg[i]]}
        
        # collect data (skip first since alread read)
        for fname in fnames_sorted[1:]:
            time.read_ippl_timing(fname)
            data = time.getTiming()
            
            tmin, tavg, tmax = self.__collect(data, labels_sorted)
            
            for i in range(len(tmin)):
                fdata[labels_sorted[i]]['min'].append(float(tmin[i]))
                fdata[labels_sorted[i]]['max'].append(float(tmax[i]))
                fdata[labels_sorted[i]]['avg'].append(float(tavg[i]))
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        for label in labels_sorted:
            ax.errorbar(cores_sorted, fdata[label]['avg'],
                        yerr=[fdata[label]['min'], fdata[label]['max']], fmt='--o')
        
        ax.grid(grid)
        plt.xlabel('#cores')
        plt.ylabel('time [s]')
        plt.xlim([0.5*cores_sorted[0], 1.05*cores_sorted[-1]])
        ax.legend(labels_sorted, loc='best')
        plt.tight_layout()
        
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
            
        
    def __collect(self, data, labels):
        tmin = []
        tmax = []
        tavg = []
        
        for label in labels:
            for d in data:
                if label == d['what'] and 'cpu max' in d: 
                    tmin.append(d['cpu avg'] - d['cpu min'])
                    tmax.append(d['cpu max'] - d['cpu avg'])
                    tavg.append(d['cpu avg'])
        
        return tmin, tavg, tmax
    
    
    def summary_plot(self, fname, **kwargs):
        """
        Create a plot with minimum, maximum and average timings
        
        Parameters
        ----------
        fname               (str)   timing file
        saveas              (str)   export the summary plot
        figsize=(12, 9)             size of the figure
        grid=False          (bool)  show grid
        
        Notes
        -----
        Throws an exception if file does not exist.
        
        Returns
        -------
        None
        """
        
        if not os.path.isfile(fname):
            raise RuntimeError("The file " + "'" + fname + "'" + " does not exist.")
        
        # get properties
        saveas = kwargs.get('saveas', None)
        figsize = kwargs.get('figsize', (12, 9))
        grid = kwargs.get('grid', False)
        
        time = timing()
        time.read_ippl_timing(fname)
        data = time.getTiming()
        
        labels = []
        tmin = []
        tmax = []
        tavg = []
        
        for d in data:
            label = d['what']
            
            if not 'main' in label:
                labels.append(label)
                tmin.append(d['cpu avg'] - d['cpu min'])
                tmax.append(d['cpu max'] - d['cpu avg'])
                tavg.append(d['cpu avg'])
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        n = len(tavg)
        x = np.linspace(0, n-1, n) 
        ax.errorbar(x, tavg, yerr=[tmin, tmax], fmt='o')
        plt.xlim([-1, n])
        plt.ylim([-10, max(tmax)+max(tavg)])
        plt.ylabel('time [s]')
        plt.xticks(x, labels, rotation='vertical')
        plt.grid(grid)
        plt.tight_layout()
        
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
    
    
    def pie_plot(self, fname, **kwargs):
        """
        Create a pie plot of the first N most time consuming timings.
        
        Parameters
        ----------
        fname               (str)   timing file
        property='cpu max'  (str)   the key of the dictionary to plot
                                    possible keys:
                                        - cpu max
                                        - cpu avg
                                        - cpu min
                                        - wall max
                                        - wall avg
                                        - wall min
        first=None          (int)   take only the first N specialized
                                    timings
        saveas              (str)   export the pie chart
        cmap_name='YlGn'    (str)   color scheme
        figsize=(12, 9)             size of the figure
        
        Notes
        -----
        Throws an exception if file not available or the key is not part
        of the dictionary
        
        Returns
        -------
        None
        """
        
        if not os.path.isfile(fname):
            raise RuntimeError("The file " + "'" + fname + "'" + " does not exist.")
        
        # get properties
        prop = kwargs.get('property', 'cpu max')
        first = kwargs.get('first', None)
        saveas = kwargs.get('saveas', None)
        cmap_name = kwargs.get('cmap', 'YlGn')
        figsize = kwargs.get('figsize', (12, 9))
        
        time = timing()
        time.read_ippl_timing(fname)
        data = time.getTiming()
        
        times_sorted, labels_sorted = self.__getMostTimeConsuming(first, data, prop)
        
        # 15. Jan. 2017, https://gist.github.com/vals/5257113
        cmap = plt.get_cmap(cmap_name)
        colors = cmap(np.linspace(0, 1, len(times_sorted)))
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.0, 0.01, 0.75, 0.98])

        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/7082345/how-to-set-the-labels-size-on-a-pie-chart-in-python
        patches, texts, autotexts = ax.pie(times_sorted,
                                           autopct='%1.1f%%',
                                           pctdistance=0.6,
                                           startangle=90,
                                           colors=colors,
                                           radius=1.0,
                                           shadow=False)
        
        # cosmetics
        for t in texts:
            t.set_fontsize(18)
            
        for at in autotexts:
            at.set_fontsize(16)
        
        ax.legend(patches, labels_sorted, loc='best', bbox_to_anchor=(1.0, 0.98), borderaxespad=0.1)
        #plt.tight_layout()
        plt.axis('equal')
        
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
            
    
    def __getMostTimeConsuming(self, n, data, prop, main=False):
        """
        Retturn time and label of the first n most time
        consuming timings.
        
        Parameters
        ----------
        n       (int)   number of timings
        data    ([{}])  timing data of one file
        prop    (str)   what property should be compared
                        possible keys:
                            - cpu max
                            - cpu avg
                            - cpu min
                            - wall max
                            - wall avg
                            - wall min
        main    (bool)  use also main timer
        
        Returns
        -------
        sorted times and labels
        """
        
        if not data:
            raise RuntimeError('No data available.')
        
        if prop not in data[1]:
            raise KeyError('This property is not part of the dictionary.')
        
        labels = []
        times = []
        
        if n == None or n > len( data ) - 1:
            # do all
            n = len( data ) - 1 # without main timing --> -1
        elif n < 1:
            raise RuntimeError("Can't plot the first " + str(n) + " timings.")
        
        for d in data:
            label = d['what']
            
            # this is really ugly!!!
            if ('main' in label) and main and (prop in d):
                labels.append(label)
                times.append(d[prop])
            
            if not 'main' in label:
                labels.append(label)
                times.append(d[prop])
            
        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/9543211/sorting-a-list-in-python-using-the-result-from-sorting-another-list
        times_sorted, labels_sorted = zip(*sorted(zip(times, labels),
                                                  key=itemgetter(0),
                                                  reverse=True))
        
        return times_sorted[0:n], labels_sorted[0:n]
