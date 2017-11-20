import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import os

import timing.Timing as timing

class TimePlot:
    
    
    def boxplot(self, fnames, **kwargs):
        """
        Create a boxbplot of several timing files
        """
        
        # get properties
        saveas = kwargs.get('saveas', None)
        cmap_name = kwargs.get('cmap', 'YlGn')
        figsize = kwargs.get('figsize', (12, 9))
        grid = kwargs.get('grid', False)
        
        
        time = timing()
        
        for fname in fnames:
            
            if not os.path.isfile(fname):
                raise RuntimeError("The file " + "'" + fname + "'" + " does not exist.")
            
            time.read_ippl_timing(fname)
            data = time.getTiming()
            
            
            
    
    def summary_plot(self, fname, **kwargs):
        """
        Create a plot with minimum, maximum and average timings
        
        Parameters
        ----------
        fname               (str)   timing file
        saveas              (str)   export the summary plot
        cmap_name='YlGn'    (str)   color scheme
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
        cmap_name = kwargs.get('cmap', 'YlGn')
        figsize = kwargs.get('figsize', (12, 9))
        grid = kwargs.get('grid', False)
        
        time = timing()
        time.read_ippl_timing(fname)
        data = time.getTiming()
        
        cmap = plt.get_cmap(cmap_name)
        colors = cmap(np.linspace(0, 1, len(data)))
        
        labels = []
        tmin = []
        tmax = []
        tavg = []
        
        for d in data:
            label = d['what']
            
            if not 'main' in label:
                labels.append(label)
                tmin.append(d['cpu min'])
                tmax.append(d['cpu max'])
                tavg.append(d['cpu avg'])
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        
        n = len(tavg)
        x = np.linspace(0, n-1, n) 
        ax.errorbar(x, tavg, yerr=[tmin, tmax], fmt='o')
        plt.xlim([-1, n])
        plt.ylim([-10, 2 * max(tmax)])
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
        
        
        if not data:
            raise RuntimeError('No data available.')
        
        if prop not in data[1]:
            raise KeyError('This property is not part of the dictionary.')
        
        labels = []
        times = []
        
        if first == None or first > len( data ) - 1:
            # do all
            first = len( data ) - 1 # without main timing --> -1
        elif first < 1:
            raise RuntimeError("Can't plot the first " + str(first) + " timings.")
        
        for d in data:
            label = d['what']
            
            if not 'main' in label:
                labels.append(label)
                times.append(d[prop])
            
        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/9543211/sorting-a-list-in-python-using-the-result-from-sorting-another-list
        times_sorted, labels_sorted = zip(*sorted(zip(times, labels),
                                                  key=itemgetter(0),
                                                  reverse=True))
        
        # 15. Jan. 2017, https://gist.github.com/vals/5257113
        cmap = plt.get_cmap(cmap_name)
        colors = cmap(np.linspace(0, 1, len(times_sorted)))
        
        fig = plt.figure(figsize=figsize)
        ax = fig.add_axes([0.0, 0.01, 0.75, 0.98])

        # 15. Jan. 2017,
        # http://stackoverflow.com/questions/7082345/how-to-set-the-labels-size-on-a-pie-chart-in-python
        patches, texts, autotexts = ax.pie(times_sorted[0:first],
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
        
        ax.legend(patches, labels_sorted[0:first], loc='best', bbox_to_anchor=(1.0, 0.98), borderaxespad=0.1)
        #plt.tight_layout()
        plt.axis('equal')
        
        if saveas:
            plt.savefig(saveas)
        else:
            plt.show()
