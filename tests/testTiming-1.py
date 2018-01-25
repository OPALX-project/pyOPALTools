import timing.Timing as Timing

time = Timing()

time.read_ippl_timing('testData/timings/timing_knl_1core.dat')

print ( time )

timing = time.getTiming()


time.read_ippl_timing('testData/timings/timing_problemsize.dat')

print ( time )

problem = time.getProblemSize()

for k, v in problem.items():
    print (k, v)
