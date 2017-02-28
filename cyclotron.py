from utils import tableau20

import numpy as np
import scipy as sp

from matplotlib import rc
import matplotlib.pylab as plt

import re

# stores the turnseparation

global ts_m
global energy_m
global phases_m
global phaseProbeNames_m
global radius_m
global phi_r_m

#
# functions associated with track-orbit computations
#
def calcTurnSeparation(filename):
    """ Calculate turn separation from OPAL xxx--trackOrbit.dat file

    Parameters
    ----------
    filename : the xxx--trackOrbit.dat
    
    Returns
    -------
    none
    
    Notes
    -----
    set the internal data structure ts_m

    References
    ----------
    none

    Examples
    --------
    Check testCycl-1.py in the test directory

    """

    global ts_m, energy_m, phi_r_m, radius_m
    headers = ["ID","x","betx","y","bety","z","betz"]
    df = np.genfromtxt(filename,
                       dtype       = None,
                       names       = headers,
                       skip_header = 2) # skip first two lines

    x=df['x']
    y=df['y']
    
    # Get x-axis crossings
    pksx = detect_peaks(x, mph=0.04, mpd=100)
    mx=x[pksx]

    # Turn separation is the difference between crossings
    ts_m=np.diff(mx)

    # Particle energy
    p_mass = 938.28 # proton mass in MeV / c^2
    # Beta*gamma
    beta_gamma = np.sqrt(df['betx']*df['betx']+df['bety']*df['bety']+df['betz']*df['betz'])
    # Gamma
    gamma = np.sqrt(1+beta_gamma*beta_gamma)
    # Energy
    energy = (gamma - 1) * p_mass
    # Radius
    radius = np.sqrt(x*x+y*y)
    # Radial direction v_r (normalise with momentum?)
    phi_r = np.arctan(df['betx']/df['bety']) - np.arctan(y/x)
    
    # Mask
    energy_m = energy[pksx]
    radius_m = radius[pksx]
    phi_r_m  = phi_r[pksx]

def calcCenteringExtraction(turnCorrection=1.35,phaseCorrection=0.0,amplitudeCorrection=1):
    """ Calculate betatron tune values and zentrierung

    Based on Fortran routine from Martin Humbel
    "Bestimmung der horizontalen Betatronschwingungsgroessen R0, DR, A und B mit der Methode der Normalengleichung"

    Parameters
    ----------
    turnCorrection      : Betatron oscillations per turn (tune), default value based on PSI Ring
    phaseCorrection     : Phase correction for betatron calculation in grad (radial angle between measurement and extraction)
    amplitudeCorrection : Amplitude correction for betatron calculation

    Returns
    -------
    None

    Notes
    -----
    Sets the internal data structure centering_m

    Examples
    --------
    TODO

    """

    global centering_m, radius_m

    # Use last 7 turns
    totalTurns = len(radius_m)
    turnsToAnalyse = min(7,totalTurns)
     
    centering_m = np.zeros(4) # R0, DR, sine (aka E), cosine (aka F)
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

        B[0] += radius_m[turnNumber]
        B[1] += radius_m[turnNumber] * turnsFromExtraction
        B[2] += radius_m[turnNumber] * cosq
        B[3] += radius_m[turnNumber] * sinq

    # Make A symmetric
    for i in range(0,dim):
        for j in range(i+1,dim):
            A[j][i] = A[i][j]
    
    # No solution for 3 and 4 turns
    if (turnsToAnalyse == 3 or turnsToAnalyse == 4):
        centering_m[0] = radius_m[turnsToAnalyse-1]
        centering_m[1] = radius_m[turnsToAnalyse-1] - radius_m[turnsToAnalyse-2]
        return
    
    # Solve linear equations Ax = B
    (lu,piv)  = sp.linalg.lu_factor(A)
    centering = sp.linalg.lu_solve((lu,piv),B)
    
    # Correction factors
    phaseCorrInRad = phaseCorrection * np.pi / 180.;
    centering_m[0] = centering[0]
    centering_m[1] = centering[1]
    centering_m[2] = amplitudeCorrection * ( centering[2]*np.cos(phaseCorrInRad) + centering[3]*np.sin(phaseCorrInRad))
    centering_m[3] = amplitudeCorrection * (-centering[2]*np.sin(phaseCorrInRad) + centering[3]*np.cos(phaseCorrInRad))
    print 'Centering values [R0,DR,E,F] =',centering_m

def getTurnSeparation():
    return ts_m

def getTurnCount():
    return len(ts_m)

def getEnergy():
    return energy_m

def getRadius():
    return radius_m

def getRadialDirection():
    return phi_r_m

def getCentering():
    return centering_m

def writeTurnSeparationToFile(fn):
    out_file = open(fn, 'w')
    for turn_sep in ts_m:
          out_file.write("%s\n" % turn_sep)

def plotTurnSeparation(figureNumber=1, asFunctionOfTurnNumber=True, asFunctionOfEnergy=False,**kwargs):
    fig=plt.figure(figureNumber,figsize=(18,6))
    #ax=plt.subplot(111)
    if asFunctionOfTurnNumber:
        x = np.arange(2, getTurnCount()+2) # From second turn
        plt.xlabel('Turn Number')
    elif asFunctionOfEnergy:
        x = getEnergy()[1:] # From second turn
        plt.xlabel('Energy [MeV]')
    else:
        x = getRadius()[1:] / 1000. # From second turn, in meters
        plt.xlabel('Radius [m]')

    plt.plot(x,getTurnSeparation(), 'o-', linewidth=2, **kwargs)
    plt.ylabel('Turn Separation [mm]')
    plt.show()

def plotBetaBeat(figureNumber=1, **kwargs):
    fig=plt.figure(figureNumber,figsize=(18,6))
    x = getRadius() / 1000. # in meters
    plt.plot(x,getRadialDirection(), 'o-', linewidth=2, **kwargs)
    plt.xlabel('Radius [m]')
    plt.ylabel('Radial Direction [rad]')
    plt.show()

def plotCentering(figureNumber=1, **kwargs):
    fig=plt.figure(figureNumber,figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1)
    x = getCentering()
    plt.plot(x[2], x[3], 'o', **kwargs)
    # Add circles
    circle1 = plt.Circle((0, 0), radius=2, fc='black', fill=False)
    plt.gca().add_artist(circle1)
    circle2 = plt.Circle((0, 0), radius=4, fc='black', fill=False)
    plt.gca().add_artist(circle2)
    
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    # Eliminate upper and right axes
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    
    # Show ticks in the left and lower axes only
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.xlabel('E')
    plt.ylabel('F')
    ax.xaxis.set_label_coords(0.9, -0.025)
    ax.yaxis.set_label_coords(-0.025,0.9)

    plt.show()

def calcRFphases(fn,RFcavity):
    """ Calculate the phases of individual cavities in the simulation
    

    Parameters
    ----------
    fn : the filename with the std out of OPAL
    RFcavity: name of the RFcavity as specifed in the input file
    Returns
    -------
    none
    

    Notes
    -----
    set the internal data structure phases_m

    References
    ----------
    none

    Examples
    --------
    Check testCycl-2.py in the test directory

    """
    global phases_m
    global phaseProbeNames_m
    phases_m = []
    phaseProbeNames_m = RFcavity

    for i,cname in enumerate(getRFphaseProbeNames()):
        turnNumber = 1
        file = open(fn, "r")
        turns  = []
        phases = []
        for line in file:
            if re.search("Finished turn",line):
                turnNumber += 1
            if re.search(cname, line):
                phase = float(line.split()[5])
                turns.append(turnNumber)
                phases.append(phase)
        phases_m.append([turns,phases])
        file.close()
            
def getRFphaseProbeNames():
        return phaseProbeNames_m

def getRFphases(i):
        return phases_m[i]

def plotRFphases(**kwargs):
    fig=plt.figure(figsize=(8,6))
    ax=plt.subplot(111)
    for i,cname in enumerate(getRFphaseProbeNames()):
        turns  = getRFphases(i)[0]
        phases = getRFphases(i)[1]
        plt.plot(turns, phases, linewidth=3, label=cname, **kwargs)
    plt.xlabel("Turn number")
    plt.ylabel("RF phase [deg]")
    plt.legend(loc=0)
    plt.show()

def plotOrbit(filename, figureNumber=1, **kwargs):
    """Plots orbit in x-y from OPAL trackOrbit.dat

    """
    headers = ["ID","x","betx","y","bety","z","betz"]
    data = np.genfromtxt(filename,
                         dtype       = None,
                         names       = headers,
                         skip_header = 2) # skip first two lines

    fig = plt.figure(figureNumber,figsize=(8,8))
    plt.plot(data['x']/1000, data['y']/1000, linewidth=1, **kwargs)
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.show()

# Using detect_peaks module for peak detection

__author__ = "Marcos Duarte, https://github.com/demotu/BMC"
__version__ = "1.0.4"
__license__ = "MIT"

def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

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

