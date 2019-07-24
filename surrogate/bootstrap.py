from sklearn.model_selection import LeavePOut
from sklearn.utils import resample
import numpy as np
import matplotlib.pyplot as plt

def plot_confidence(y, y_pred, y_lo, y_up, alpha):
    plt.scatter(y, y_pred, marker='.')
    plt.plot([min(y), max(y)], [min(y), max(y)], 'k--')
    plt.fill_between(y, y_lo, y_up, alpha=0.2, label='CI ' + str(alpha) + ' %')
    plt.xlabel('high fidelity model')
    plt.ylabel('surrogate model')
    return plt


class Bootstrap:
    def __init__(self, estimator):
        self._estimator = estimator

        self._sample = {
            'random':   Random,
            'loo':      LOO,
            'lpo':      LPO,
        }

        self._computed = False

    def boot(self, x, y, sample='random', **kwargs):
        if not sample in self._sample.keys():
            raise RuntimeError("No sampling method '" + sample + "'.")

        self._x = x
        self._y = y

        self.sampler = self._sample[sample](x, **kwargs)

        self._data = []
        n_boot = self.sampler.n_boot
        for i in range(n_boot):
            x_train, y_train = self.sampler.get_next(x, y)
            self._estimator.fit(x_train, y_train)
            self._data.append( self._estimator.fitted_ )
        self._computed = True


    def confidence_interval(self, alpha):
        """
        X:  NxD
        y:  Nx1

        https://stat.ethz.ch/education/semesters/ss2016/CompStat/sk.pdf
        """
        if not self._computed:
            raise RuntimeError("Bootstrapping not yet performed.")
        self._computed = False

        alpha = 1.0 - alpha

        qlo = np.percentile(self._data, q=(1.0 - 0.5 * alpha)*100, axis=0)
        qhi = np.percentile(self._data, q=(0.5 * alpha)*100, axis=0)

        self._estimator.fit(self._x, self._y)

        fitted = self._estimator.fitted_

        return 2.0 * fitted - qlo, 2.0 * fitted - qhi


class Sample(object):

    def __init__(self, n_boot):
        self.n_boot = n_boot

    def get_next(self, x, y):
        pass


class LPO(Sample):
    def __init__(self, x, **kwargs):
        p = kwargs.pop('p', 1)
        self._lpo = LeavePOut(p)
        self._splits = self._lpo.split(x)
        super(LPO, self).__init__(self._lpo.get_n_splits(x))

    def get_next(self, x, y):
        train_index = next(self._splits)[0]
        return x[train_index], y[train_index]


class LOO(LPO):
    def __init__(self, x):
        super(LOO, self).__init__(x, p=1)


class Random(Sample):
    def __init__(self, x, **kwargs):
        n_boot          = kwargs.pop('n_boot', 100)
        self.replace    = kwargs.pop('replace', True)
        self.n_samples  = kwargs.pop('n_samples', None)
        super(Random, self).__init__(n_boot)

    def get_next(self, x, y):
        x_train, y_train = resample(x, y,
                                    replace=self.replace,
                                    n_samples=self.n_samples)
        return x_train, y_train
