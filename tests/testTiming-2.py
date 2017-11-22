import timing.TimePlot as TimePlot

tplot = TimePlot()

tplot.pie_plot(fname = 'testData/timings/timing_bdw_16cores.dat', cmap='viridis_r',
               first=7)

tplot.summary_plot(fname='testData/timings/timing_bdw_16cores.dat', grid=True, title='Timing summary')

tplot.line_plot(['testData/timings/timing_bdw_1core.dat',
                'testData/timings/timing_bdw_2core.dat',
                'testData/timings/timing_bdw_8core.dat',
                'testData/timings/timing_bdw_4core.dat',
                'testData/timings/timing_bdw_16cores.dat'], first=5)
