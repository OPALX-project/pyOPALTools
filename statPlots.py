from utils import tableau20
from utils import SddsReader
import numpy as np

from matplotlib import rc
import matplotlib.pylab as plt


enu = ['a) ','b) ', 'c)' ]    

def opalStatOverviewPlot(fns, title="", pdfFn="", addData=[], myLoc=2):
    
    """ 
    Plot an overview of results form possible 
    several stat files. If pdfFn is given a PDF-File is written

    Example:

    import statPlots as statpl
    
    fns = []
    fns.append('xxx/foo1.stat')
    fns.append('xxx/foo2.stat')

    statpl.opalStatOverviewPlot(fns)
    
    
    Parameters
    ----------
    fns
    title
    pdfFn 
    addData=[]
    myLoc=2
    
    Returns
    -------
    none
    

    Notes
    -----
    

    References
    ----------
    none

    Examples
    --------
    Check testStat-1.py in the test directory
    """
    
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)
    
    params = {
        'axes.labelsize': 8,
        'text.fontsize': 8,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.usetex': False,
        'figure.figsize': [20, 15]
        }

    rc(params)
    sparsePlot = True
    
    xrms = []
    yrms = []
    zrms = []

    exrms = []
    eyrms = []
    ezrms = []

    E     = []
    dE    = []
    x     = []

    additionalData = []

    dataSrc = []
    

    for i in range(len(fns)):
        
        dataSrc.append(fns[i].split("/")[-2]+'/'+fns[i].split("/")[-1])
        parser = SddsReader(fns[i])

        if not x:
            x = parser.getColumn("s")            # we assume for all plots the same x axis

        xrms.append(parser.getColumn("rms_x"))
        yrms.append(parser.getColumn("rms_y"))
        zrms.append(parser.getColumn("rms_s"))

        exrms.append(parser.getColumn("emit_x"))
        eyrms.append(parser.getColumn("emit_y"))
        ezrms.append(parser.getColumn("emit_s"))
        
        E.append(parser.getColumn("energy"))
        dE.append(parser.getColumn("dE"))

        if addData:
            additionalData.append(parser.getColumn(addData[0][0]))

    # rescale

    exrms[0]  = map(lambda x: x * 1.0e6, exrms[0] )
    eyrms[0]  = map(lambda x: x * 1.0e6, eyrms[0] )
    ezrms[0]  = map(lambda x: x * 1.0e6, ezrms[0] )

    xrms[0]  = map(lambda x: x * 1.0e3, xrms[0] )
    yrms[0]  = map(lambda x: x * 1.0e3, yrms[0] )
    zrms[0]  = map(lambda x: x * 1.0e3, zrms[0] )

    # plot with various axes scales
    fig = plt.figure(figsize=(20,15))
    print dataSrc
    if len(dataSrc)>1:
        l = []
        l.append(title)
        for i in range(len(dataSrc)):
            l.append(enu[i]+dataSrc[i]+' \n')
        s=''.join(l)
        fig.suptitle(s, fontsize=14, fontweight='bold')
    else:
        fig.suptitle(title+dataSrc[0], fontsize=14, fontweight='bold')

    sp1 = plt.subplot(221)
    if sparsePlot:
        sp1.spines["top"].set_visible(False)    
        sp1.spines["bottom"].set_visible(False)    
        sp1.spines["right"].set_visible(False)    
        sp1.spines["left"].set_visible(False)
        sp1.get_xaxis().tick_bottom()    
        sp1.get_yaxis().tick_left() 
    for i in range(len(fns)):
        plt.plot(x, xrms[i], linewidth=3, color=tableau20[i])
        plt.plot(x, yrms[i], linewidth=3, color=tableau20[i+2])
        plt.plot(x, zrms[i], linewidth=3, color=tableau20[i+6])

    legend = plt.legend(getLegendStr(['x','y','z'],dataSrc,enu), loc=myLoc);
    frame = legend.get_frame()
    frame.set_facecolor('1.0')
    frame.set_edgecolor('1.0')
    
    plt.xlabel('s (m)')
    plt.ylabel('Beamsize (mm)')
    plt.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
#    plt.xticks(np.arange(0, 30, 5))

    sp2 = plt.subplot(222)
    if sparsePlot:
        sp2.spines["top"].set_visible(False)    
        sp2.spines["bottom"].set_visible(False)    
        sp2.spines["right"].set_visible(False)    
        sp2.spines["left"].set_visible(False)
        sp2.get_xaxis().tick_bottom()    
        sp2.get_yaxis().tick_left() 

    for i in range(len(fns)):
        plt.plot(x, exrms[i], linewidth=3, color=tableau20[i])
        plt.plot(x, eyrms[i], linewidth=3, color=tableau20[i+2])
        plt.plot(x, ezrms[i], linewidth=3, color=tableau20[i+6])

    legend = plt.legend(getLegendStr(['$\epsilon_x$', '$\epsilon_y$', '$\epsilon_z$'],dataSrc,enu), loc=myLoc);
    frame = legend.get_frame()
    frame.set_facecolor('1.0')
    frame.set_edgecolor('1.0')

    plt.xlabel('s (m)')
    plt.ylabel('Emittance (mm-mrad)')
    plt.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
#    plt.xticks(np.arange(0, 30, 5))

    sp3 = plt.subplot(223)
    if sparsePlot:
        sp3.spines["top"].set_visible(False)    
        sp3.spines["bottom"].set_visible(False)    
        sp3.spines["right"].set_visible(False)    
        sp3.spines["left"].set_visible(False)
        sp3.get_xaxis().tick_bottom()    
        sp3.get_yaxis().tick_left() 

    for i in range(len(fns)):
        plt.semilogy(x, E[i], linewidth=3, color=tableau20[i])
        plt.semilogy(x, dE[i], linewidth=3, color=tableau20[i+2])

    legend = plt.legend(getLegendStr(['E ', '$\Delta$E'], dataSrc, enu), loc=myLoc);
    frame = legend.get_frame()
    frame.set_facecolor('1.0')
    frame.set_edgecolor('1.0')

    plt.xlabel('s (m)')
    plt.ylabel('Energy and Energyspread  (MeV)')
    plt.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
#    plt.xticks(np.arange(0, 30, 5))

    sp4 = plt.subplot(224)
    if sparsePlot:
        sp4.spines["top"].set_visible(False)    
        sp4.spines["bottom"].set_visible(False)    
        sp4.spines["right"].set_visible(False)    
        sp4.spines["left"].set_visible(False)
        sp4.get_xaxis().tick_bottom()    
        sp4.get_yaxis().tick_left() 

    if addData:
        for i in range(len(fns)):
            plt.plot(x, additionalData[i], linewidth=3, color=tableau20[i])

        legend = plt.legend(getLegendStr([addData[0][1]],dataSrc,enu), loc=myLoc);
        frame = legend.get_frame()
        frame.set_facecolor('1.0')
        frame.set_edgecolor('1.0')
        plt.xlabel('s (m)')

    if pdfFn:
        plt.savefig(pdfFn)

    plt.show()
 

def opalStatPlot(x,y,ylegend,xaxis="",yaxis="",title="", pdfFn=""):
    '''
    Plot several collumns from an OPAL stat file. If
    pdfFn is given a PDF-File is written

    Example:

    import statPlots as statpl
    from utils import SddsReader
    
    fn = 'xxx/foo.stat'
    parser = SddsReader(fn)

    x = parser.getColumn("s")
    y = []
    y.append(parser.getColumn("rms_x"))
    y.append(parser.getColumn("rms_y"))
    y.append(parser.getColumn("rms_s"))

    ylegend = []
    ylegend.append("rmsx")
    ylegend.append("rmsy")
    ylegend.append("rmss")

    xlabel = "s (m)"
    ylabel = "Beamsize (m)"
    title  = "My Plot"
    statpl.opalStatPlot(x,y,ylegend,xlabel,ylabel,title,plotfn)
    
    Parameters
    ----------
    fns
    title
    pdfFn 
    addData=[]
    myLoc=2
    
    Returns
    -------
    none
    

    Notes
    -----
    

    References
    ----------
    none

    Examples
    --------
    Check testStat-2.py in the test directory
    '''
    for i in range(len(tableau20)):
        r, g, b = tableau20[i]
        tableau20[i] = (r / 255., g / 255., b / 255.)

    params = {
        'axes.labelsize': 8,
        'text.fontsize': 8,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.usetex': False,
        'figure.figsize': [4.5, 4.5]
        }
    rc(params)

    for i in range(len(y)):
        plt.plot(x, y[i], linewidth=2, color=tableau20[i])

    legend = plt.legend(ylegend, loc=4);
    frame = legend.get_frame()
    frame.set_facecolor('1.0')
    frame.set_edgecolor('1.0')
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
    plt.xticks(np.arange(0, 30, 5))
    if pdfFn:
        plt.savefig(pdfFn)
    plt.show()

#
# Functions related to job plotting stat data
#

def getLegendStr(s,dataSrc,enu):

    if len(dataSrc)>1:
        l = []
        for i in range(len(dataSrc)):
            for j in range(len(s)):
                l.append(enu[i] + s[j])
        return l
    else:
        return s
