import utils as ut


fn = 'testData/Accelerated.h5'

h5 = ut.H5Reader(fn)

k  = h5.getKurtosis('/x',-1)

print k
