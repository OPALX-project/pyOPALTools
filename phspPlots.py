from utils import tableau20
from utils import H5Reader
from utils import tickLabel

from matplotlib import rc
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm

import scipy
from scipy import stats
import numpy as np

def plotOPALPhaseSpaceContours(fn, step=1, label='', xlim=[1820,1860], xlabel='x (mm)', ylabel='px (beta gamma) * 1e3', pdfFn='Hist1d.pdf', bins=500) :
    '''
     Plot phase sapce with 3 contours levels
     
    '''
    gs1 = gridspec.GridSpec(1, 1)  
                                                                                                                          
    fig=plt.figure(figsize=(9,12))

    ax = plt.subplot(gs1[0])
       
    plt.setp(ax.get_xticklabels(), visible=False)
    
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    h5 = H5Reader(fn)
    
    x=h5.getStepData(step,'x')*1000.0
    y=h5.getStepData(step,'px')*1000.0

    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    
    plotData(x,y,ax)
    
    tickLabel(ax)

    big_ax = fig.add_subplot(111)
    big_ax.set_axis_bgcolor('none')
    big_ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    big_ax.set_xlabel(xlabel,family='serif',fontsize=16)
    big_ax.set_ylabel(ylabel,family='serif',fontsize=16)
    fig.tight_layout()
    plt.show()
    plt.savefig(pdfFn)
    return
    

def percentileScore(kernel,percentile,NSamples):
    s=scipy.stats.scoreatpercentile(kernel(kernel.resample(NSamples)), 100-percentile)
    return s

def plotData(x,y,ax):
    
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    
    
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]

    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)

    xgrid=np.linspace(xmin,xmax,100)
    ygrid=np.linspace(ymin,ymax,100)

    q,w=np.meshgrid(xgrid, ygrid)
    r=kernel([q.flatten(),w.flatten()])

    # sample the pdf and find the value at each percentile                                                                                                                                     
    s1=percentileScore(kernel,99.7,5000)
    s2=percentileScore(kernel,95.0,5000)
    s3=percentileScore(kernel,68.0,1000)
    s100=percentileScore(kernel,0,1000)

    # reshape back to 2d                                                                                                                                                                       
    r.shape=(ygrid.size,xgrid.size)

    # plot the contour at each percentile                                                                                                                                                      
    norm = cm.colors.Normalize(vmax=abs(r).max(), vmin=0)
    ax.contourf(xgrid, ygrid, r, [s1,s2,s3,np.amax(r)],cmap='Blues',norm=norm)
    cset = ax.contour(xgrid, ygrid, r, [s1,s2,s3],linewidths=2, colors='k')

    fmt = {}
    strs = ['99.7 %','95 %','68 %']
    for l, s in zip(cset.levels, strs):
        fmt[l] = s
    ax.clabel(cset,cset.levels, inline=True,fmt=fmt, fontsize=14)
    return 0