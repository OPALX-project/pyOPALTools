
import phspPlots as plt
import utils as ut

what=['x','py']

scale=[1000.,1000.]

step=0

fn = 'testData/Accelerated.h5'

h5 = ut.H5Reader(fn)

plt.plotOPALPhaseSpace(fn,what,scale,step)

plt.plotOPALPhaseSpaceContours(fn,what,scale,h5.getSteps())