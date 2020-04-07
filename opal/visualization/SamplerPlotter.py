from .BasePlotter import *
import numpy as np

from .formatter import FormatScalarFormatter
import os



class SamplerPlotter(BasePlotter):

    def __init__(self):
        pass


    def plot_variability(self, fname, xvar, yvar, **kwargs):
        """Plot the mean, min and max over all samples.

        Parameters
        ----------
        fname : str
            File containing the data (xvar and yvar)
        xvar : str
            x-axis data
        yvar : str
            y-axis data
        idx : bool, optional
            Fix the x-axis labels (takes the original
            data order but uses the indices to plot
            and the values as ticks), useful for
            periodic values (e.g. azimuth)
        nticks : int, optional
            Number of ticks on axes (only for idx=True)

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            from opal import load_dataset

            nsamples = self.ds.size

            dirname = os.path.dirname(self.ds.filename)
            sdir = os.path.join(dirname, str(0))
            out = load_dataset(sdir, fname=fname, info=False)
            ydata = np.zeros(out.size, dtype=np.float)
            ymin  = np.finfo(np.float).max + np.zeros(out.size, dtype=np.float)
            ymax  = np.finfo(np.float).min + np.zeros(out.size, dtype=np.float)

            xdata = out.getData(xvar, **kwargs)

            nticks = kwargs.pop('nticks', 10)

            for i in range(nsamples):
                # load simulation directory
                sdir = os.path.join(dirname, str(i))
                out = load_dataset(sdir, fname=fname, info=False)
                data = out.getData(yvar, **kwargs)
                ydata += data
                ymin = np.minimum(ymin, data)
                ymax = np.maximum(ymax, data)

            mean = np.zeros(len(ydata), dtype=np.float)
            mean = ydata / np.float(nsamples)

            if not kwargs.pop('idx', False):
                plt.plot(xdata, mean, **kwargs, color='black', linestyle='dashed', label='mean')
                plt.fill_between(xdata, ymin, ymax,
                                facecolor='blue', alpha=0.2, label='variability region')
            else:
                l = len(xdata)
                ind = np.linspace(0, l-1, l, dtype=int)
                plt.plot(ind, mean, **kwargs, color='black', linestyle='dashed', label='mean')
                plt.fill_between(ind, ymin, ymax,
                                facecolor='blue', alpha=0.2, label='variability region')
                t = int(l / nticks) - 1
                plt.xticks(ind[::t], np.round(xdata, 0)[::t].astype(int))

            plt.legend(loc = 'upper center',
                    ncol=2, labelspacing=0.5,
                    bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))

            plt.gca().ticklabel_format(axis='y', style='sci', scilimits=(-2, 2),
                                    useMathText=True, useOffset=True)

            xlabel = out.getLabel(xvar)
            xunit  = out.getUnit(xvar)

            ylabel = out.getLabel(yvar)
            yunit  = out.getUnit(yvar)

            plt.xlabel(xlabel + ' [' + xunit + ']')
            plt.ylabel(ylabel + ' [' + yunit + ']')
            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_sample_input_statistics(self, **kwargs):
        """Bar plot showing the number of samples per design variable.
        This makes only sense for sampling with only a few states.

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            # 10. April 2019
            # https://docs.python.org/2/library/collections.html
            from collections import Counter

            dvars = self.ds.design_variables

            nvar = len(dvars)

            counters = [Counter()] * nvar

            for i in range(self.ds.size):
                for j, dvar in enumerate(dvars):
                    counters[j][self.ds.getData(var=dvar, ind=i)] += 1

            for j, dvar in enumerate(dvars):
                # 10. April 2019
                # https://stackoverflow.com/questions/12282232/how-do-i-count-unique-values-inside-a-list
                values = counters[j].values()
                curr = 0
                for val in values:
                    plt.bar(np.arange(nvar), val, bottom=curr, width=1.0 / nvar)
                    curr += val

            plt.xticks(np.arange(nvar), dvars)
            plt.ylabel('#occurrences')

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_auto_correlation(self, ind, **kwargs):
        """Compare a sample set with itself.

        Parameters
        ----------
        ind : list
            Indices of the sample set.
        nsamples : bool, optional
            Show a horizontal line indicating
            the total number of samples
        percent : bool, optional
            Indicate the agreement in percent
            above each bar

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            import matplotlib as mpl

            percent = kwargs.pop('percent', False)

            nsamples = len(ind)
            matches = []
            ntrain = 1

            scale = 1.0
            if percent:
                scale = float(nsamples) * 0.01

            while not ntrain == nsamples:
                sample = ind[0:ntrain]
                diff = ind[ntrain:]
                matches.append( self.ds.find_matches(sample, diff) / scale )
                ntrain += 1

            plt.plot(np.arange(nsamples - 1), matches)

            isTex = mpl.rcParams['text.usetex']

            xlabel = '#samples'
            ylabel = '#identical samples'
            llabel = '#samples'
            blabel = '%'

            if isTex:
                xlabel = '\\' + xlabel
                ylabel = '\\' + ylabel
                llabel = '\\' + llabel
                blabel = '\\' + blabel

            if percent:
                ylabel = ylabel + ' in ' + blabel

            plt.xlabel( xlabel )
            plt.ylabel( ylabel )

            if kwargs.pop('nsamples', False) and not percent:
                plt.axhline(nsamples, linestyle='dashed', label=llabel)
                plt.legend(loc = 'upper center', ncol=1, labelspacing=0.,
                        bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))

            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    def plot_training_vs_validation(self, train0, **kwargs):
        """Bar plot comparing training with validation set.

        Parameters
        ----------
        train0 : list
            Indices of the training points.
        train1 : list, optional
            More lists with indices
            train2, train3, etc. are also keywords
        nsamples : bool, optional
            Show a horizontal line indicating
            the total number of samples
        percent : bool, optional
            Indicate the agreement in percent
            above each bar

        Returns
        -------
        matplotlib.pyplot
            Plot handle
        """
        try:
            import matplotlib as mpl

            nsamples = self.ds.size

            trains = [train0]
            i = 1
            while True:
                train = kwargs.pop('train' + str(i), None)
                if train == None:
                    break

                trains.append(train)
                i += 1

            matches = []
            ntrains = []
            for train in trains:
                ntrain = len(train)
                ntrains.append( ntrain )

                if ntrain >= nsamples:
                    opal_logger.error('ntrain (' + str(ntrain) + ') >= ' +
                                    'nsamples (' + str(nsamples) + ')')

                validation = np.arange(nsamples, dtype=int)

                # get all indices not in training sample set
                # 12. April 2019
                # https://stackoverflow.com/questions/3428536/python-list-subtraction-operation
                validation = [int(i) for i in validation if int(i) not in train]

                matches.append( self.ds.find_matches(train, validation) )

            ind = np.arange(len(ntrains))
            bars = plt.bar(ind, matches)
            plt.xticks(ind, ntrains)

            isTex = mpl.rcParams['text.usetex']

            xlabel = '#training samples'
            ylabel = '#identical samples with validation set'
            llabel = '#samples'
            blabel = '%'

            if isTex:
                xlabel = '\\' + xlabel
                ylabel = '\\' + ylabel
                llabel = '\\' + llabel
                blabel = '\\' + blabel

            plt.xlabel( xlabel )
            plt.ylabel( ylabel )

            topline = kwargs.pop('nsamples', False)

            if topline:
                plt.axhline(nsamples, linestyle='dashed', label=llabel)

            if kwargs.pop('percent', True):
                # 12. April 2019
                # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
                for rect in bars:
                    height = rect.get_height()
                    plt.gca().text(rect.get_x() + rect.get_width()*0.5, 1.01*height,
                                '{}'.format(height * 100.0 / nsamples) + blabel, ha='center', va='bottom')

                #self._autolabel(plt.gca(), bars, 'center')

            if topline:
                plt.legend(loc = 'upper center', ncol=1, labelspacing=0.,
                        bbox_to_anchor=(0.5, 1.1, 0.0, 0.0))

            plt.tight_layout()

            return plt
        except Exception as ex:
            opal_logger.exception(ex)
            return plt.figure()


    # 12. April 2019
    # https://matplotlib.org/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py
    def _autolabel(self, ax, rects, xpos='center'):
        """Attach a text label above each bar in *rects*, displaying its height.

        Copied from matplotlib.org. It's slightly modified.

        `xpos` indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """

        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')
