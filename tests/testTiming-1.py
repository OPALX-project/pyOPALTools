import timing.Timing as Timing

time = Timing()

time.read_ippl_timing('testData/timing.dat')

print ( time )

timing = time.getTiming()
