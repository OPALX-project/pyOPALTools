import timing.TimePlot as TimePlot

tplot = TimePlot()

tplot.pie_plot(fname = 'testData/timing.dat', cmap='viridis_r')

tplot.summary_plot(fname='testData/timing.dat', grid=True)