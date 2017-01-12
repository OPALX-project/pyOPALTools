from utils import SddsReader
import statPlots as pl

fn = 'testData/Accelerated.stat'                                                                                                                                    
plotfn = 'Accelerated.pdf'
  
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
pl.opalStatPlot(x,y,ylegend,xlabel,ylabel,title,plotfn)
