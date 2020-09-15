# Copyright (c) 2019 - 2020, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

def bootstrap_sobol(xdata, ydata, estimator, n_boot, **kwargs):
    """
    Bootstrap with replacement of Sobol indices

    Parameters
    ----------
    xdata  : numpy.ndarray
        input data (N, D) with
        N number samples
        D dimension
    ydata : numpy.ndarray
        output data (N, 1)
    estimator : BaseEstimator
        UQ model
    n_boot : int
        number of bootstraps
    n_samples : int, optional
        The bootstrap sample size. If not provided, n_samples = N
    seed : int, optional
        The seed of the numpy random number generator.

    Notes
    -----
    Implemented according to
    G. E. B. Archer, A. Saltelli & I. M. Sobol (1997)
    Sensitivity measures, anova-like Techniques and the use of bootstrap,
    Journal of Statistical Computation and Simulation, 58:2,99-120,
    DOI: 10.1080/00949659708811825

    Returns
    -------
    list
        Two lists of CI upper bounds, i.e. main sensitivities, total sensitivites
    """
    from sklearn.utils import resample
    import numpy as np

    n_samples = kwargs.pop('n_samples', None)
    seed      = kwargs.pop('seed', None)

    random_states = [None] * n_boot

    np.random.seed(seed)

    if not seed == None:
        random_states = np.random.randint(1, 1e6, size=n_boot)

    n_par = np.shape(xdata)[1]
    allsens_m = np.empty((n_boot, n_par))
    allsens_t = np.empty((n_boot, n_par))

    for i in range(n_boot):
        estimator.clear()
        xboot, yboot = resample(xdata, ydata, replace=True,
                                n_samples=n_samples, random_state=random_states[i])
        estimator.fit(xboot, yboot)
        allsens_m[i, :] = estimator.main_sensitivity()
        allsens_t[i, :] = estimator.total_sensitivity()

    std_m = np.std(allsens_m, ddof=1, axis=0)
    std_s = np.std(allsens_t, ddof=1, axis=0)

    return 1.96 * std_m, 1.96 * std_s


def bootstrap_ci(xdata, ydata, estimator, n_boot, **kwargs):
    """
    Bootstrap with replacement for confidence interval

    Parameters
    ----------
    xdata : numpy.ndarray
        input data (N, D) with
        N number samples
        D dimension
    ydata : numpy.ndarray
        output data (N, 1)
    estimator : BaseEstimator
        UQ model
    n_boot : int
        number of bootstraps
    n_samples : int, optional
        The bootstrap sample size. If not provided, n_samples = N
    seed : int, optional
        The seed of the numpy random number generator.

    Returns
    -------
    [numpy.ndarray, numpy.ndarray]
        y_lo (N, 1) evaluated at xdata
        y_up (N, 1) evaluated at xdata
    """
    from sklearn.utils import resample
    from scipy import stats
    import numpy as np

    estimator.fit(xdata, ydata)
    pccf = estimator.fitted_

    n_samples = kwargs.pop('n_samples', None)

    if n_samples == None:
        n_samples = len(ydata)

    seed = kwargs.pop('seed', None)

    random_states = [None] * n_boot

    if not seed == None:
        np.random.seed(seed)
        random_states = np.random.randint(1, 1e6, size=n_boot)

    data = np.zeros((n_boot, len(pccf)))
    for i in range(n_boot):
        estimator.clear()
        xboot, yboot = resample(xdata, ydata, replace=True,
                                n_samples=n_samples, random_state=random_states[i])
        estimator.fit(xboot, yboot)
        ll = len(estimator.fitted_)
        data[i, 0:ll] = estimator.fitted_

    se = np.std(data, ddof=1, axis=0)
    return pccf - 1.96 * se, pccf + 1.96 * se
