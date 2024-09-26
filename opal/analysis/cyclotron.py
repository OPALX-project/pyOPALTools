# Copyright (c) 2018 - 2019, Jochem Snuverink, Paul Scherrer Institut, Villigen PSI, Switzerland
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

import numpy as np
import dask.array as da
import scipy as sp

def calcCenteringExtraction(radius, turnCorrection=1.35, phaseCorrection=0.0, amplitudeCorrection=1):
    """Calculate betatron tune values and zentrierung

    Based on Fortran routine from Martin Humbel
    "Bestimmung der horizontalen Betatronschwingungsgroessen R0, DR, A und B mit der Methode der Normalengleichung"

    Parameters
    ----------
    radius : array_like
        Radii of turns
    turnCorrection : float, optional
        Betatron oscillations per turn (tune), default value (1.35) based on PSI Ring
    phaseCorrection : float, optional
        Phase correction for betatron calculation in grad
        (radial angle between measurement and extraction, default: 0)
    amplitudeCorrection : float, optional
        Amplitude correction for betatron calculation (default: 1)

    Returns
    -----
    array
        The centering values

    Examples
    --------
    Check Cyclotron.ipynb in the opal/test directory

    """

    # Use last 7 turns
    totalTurns = len(radius)
    turnsToAnalyse = min(7,totalTurns)

    centering = np.zeros(4) # R0, DR, sine (aka E), cosine (aka F)
    if (turnsToAnalyse < 2):
        return

    # Fill matrix
    dim = 4
    A = np.zeros((dim,dim))
    B = np.zeros(dim)
    for i in range(0,turnsToAnalyse):
        turnsFromExtraction = i - totalTurns + 1;
        turnNumber          = totalTurns - turnsToAnalyse + i;
        sinq = np.sin(turnsFromExtraction * 2 * np.pi * turnCorrection)
        cosq = np.cos(turnsFromExtraction * 2 * np.pi * turnCorrection)
        A[0][0] += 1
        A[0][1] += turnsFromExtraction
        A[0][2] += cosq
        A[0][3] += sinq
        A[1][1] += turnsFromExtraction * turnsFromExtraction
        A[1][2] += turnsFromExtraction * cosq
        A[1][3] += turnsFromExtraction * sinq
        A[2][2] += cosq * cosq
        A[2][3] += cosq * sinq
        A[3][3] += sinq * sinq

        B[0] += radius[turnNumber]
        B[1] += radius[turnNumber] * turnsFromExtraction
        B[2] += radius[turnNumber] * cosq
        B[3] += radius[turnNumber] * sinq

    # Make A symmetric
    for i in range(0,dim):
        for j in range(i+1,dim):
            A[j][i] = A[i][j]

    # No solution for 3 and 4 turns
    if (turnsToAnalyse == 3 or turnsToAnalyse == 4):
        centering[0] = radius[turnsToAnalyse-1]
        centering[1] = radius[turnsToAnalyse-1] - radius[turnsToAnalyse-2]
        return

    # Solve linear equations Ax = B
    (lu,piv)  = sp.linalg.lu_factor(A)
    centering = sp.linalg.lu_solve((lu,piv),B)

    # Correction factors
    phaseCorrInRad = phaseCorrection * np.pi / 180.;
    centering[0] = centering[0]
    centering[1] = centering[1]
    centering[2] = amplitudeCorrection * ( centering[2]*np.cos(phaseCorrInRad) + centering[3]*np.sin(phaseCorrInRad))
    centering[3] = amplitudeCorrection * (-centering[2]*np.sin(phaseCorrInRad) + centering[3]*np.cos(phaseCorrInRad))
    print ( 'Centering values [R0,DR,E,F] =', centering )
    return centering


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : array_like
        1D data.
    mph : None or number, optional
        Detect peaks that are greater than minimum peak height (default: None).
    mpd : int, optional
        detect peaks that are at least separated by minimum peak distance (in
        number of data, default = 1).
    threshold : int, optional
        Detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors (default = 0).
    edge : None or str
        {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional
        keep peaks with same height even if they are closer than `mpd` (default = False).
    valley : bool, optional
        If True, detect valleys (local minima) instead of peaks.
    show : bool, optional
        If True, plot data in matplotlib figure.
    ax : matplotlib.axes.Axes instance, optional

    Returns
    -------
    ind : array_like
        indices of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    >>> from detect_peaks import detect_peaks
    >>> x = np.random.randn(100)
    >>> x[60:81] = np.nan
    >>> # detect all peaks and plot data
    >>> ind = detect_peaks(x, show=True)
    >>> print(ind)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # set minimum peak height = 0 and minimum peak distance = 20
    >>> detect_peaks(x, mph=0, mpd=20, show=True)

    >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    >>> # set minimum peak distance = 2
    >>> detect_peaks(x, mpd=2, show=True)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # detection of valleys instead of peaks
    >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

    >>> x = [0, 1, 1, 0, 1, 1, 0]
    >>> # detect both edges
    >>> detect_peaks(x, edge='both', show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> # set threshold = 2
    >>> detect_peaks(x, threshold = 2, show=True)
    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind


def eval_radius(x, y):
    r"""Evaluate the radius

    .. math:: r = \sqrt{x^2 + y^2}

    Parameters
    ----------
    x : float or array
        Data of `x`-direction
    y  : float or array
        Data of `y`-direction

    Returns
    -------
    float
        Radius
    """
    r = da.sqrt(x ** 2 + y ** 2)
    return r


def eval_radial_momentum(px, py, theta):
    r"""Evaluate the radial momentum

    .. math: pr = px \cos(\theta) + py \sin(\theta)

    Parameters
    ----------
    px : float or array
        Data of momentum in `x`
    py : float or array
        Data of momentum in `y`
    theta : float
        Azimuthal angle (in radian)

    Returns
    -------
    float
        Radial momentum

    Notes
    -----
    .. math::
        \begin{align}
        x & = r \sin(\theta) \\
        y & = r \cos(\theta) \\
        r & = \sqrt(x^2 + y^2) \\
        \frac{dr}{dt} & = \frac{dr}{dx} \frac{dx}{dt} + \frac{dr}{dy} \frac{dy}{dt} \\
        \frac{dr}{dt} & \sim \textrm{radial momentum}~p_r \\
        \frac{dx}{dt} & \sim \textrm{horizontal momentum}~p_x \\
        \frac{dy}{dt} & \sim \textrm{longitudinal momentum}~p_y \\
        \frac{dr}{dx} & = \frac{1}{2 r} * 2 * x = \frac{x}{r} = \cos(\theta) \\
        \frac{dr}{dy} & = \frac{1}{2 r} * 2 * y = \frac{y}{r} = \sin(\theta) \\
        \rightarrow p_r & = p_x \cos(\theta) + p_y \sin(\theta)
        \end{align}
    """
    return px * da.cos(theta) + py * da.sin(theta)
