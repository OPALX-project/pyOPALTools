import cyclotron as cycl

cnames = []
cnames.append('RF3B')
cycl.calcRFphases('testData/Accelerated.out',cnames)
cycl.plotRFphases()


