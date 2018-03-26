import re

class LatticeParser:
	
    def __init__(self):
        self.dictPlot={}
        self.pathLattice = ''
        self.fig=None
        self.ax1=None
        self.ax2=None

        self.pattern_quadrupole=re.compile(r'''QUADRUPOLE \n
                                ''',re.VERBOSE|re.UNICODE)
        self.pattern_monitor=re.compile(r'''MONITOR \n
                                ''',re.VERBOSE|re.UNICODE)
        self.pattern_collimator=re.compile(r'''COLLIMATOR \n
                                ''',re.VERBOSE|re.UNICODE)
        self.pattern_dipole=re.compile(r'''DIPOLE \n
                                ''',re.VERBOSE|re.UNICODE)
	

      
	    self.pattern_corner=re.compile(r'''(?P<name>[A-Z,0-9]*) [\s]+            
	            (?P<one>[0-9]+ [.]? [0-9]*) [\s]*
	            ((?P<two>[0-9]+ [.]? [0-9]*) [\s]*)?
	            ((?P<three>[0-9]+ [.]? [0-9]*) [\s]*)?
	            (?P<four>[0-9]+ [.]? [0-9]*)? \s* \n
	                            ''',re.VERBOSE|re.UNICODE)
	    self.dictTypes={
	        "monitor": [pattern_monitor, 2,'k-'], 
	        "collimator":[pattern_collimator,4,'k-'],
	        "dipole": [pattern_dipole,5,'b-'],
	        "quadrupole":[pattern_quadrupole,5,'r-'],
	    }

    def plotLattice(self, pathLattice, fig, ax1, ax2):
    
        self.pathLattice = pathLattice
        self.fig = fig
        self.ax1 = ax1
        self.ax2 = ax2
        
        with open(self.pathLattice, 'r') as lattice:
            for p,line in enumerate(lattice):
                if p%2==0:
                    for eltype in self.dictTypes:
                        typematch=self.dictTypes[eltype][0].match(line)
                        if typematch:
                            element=eltype
                            break                    
                   
                if p%2==1 and typematch:
                    cornermatch= self.pattern_corner.match(line)
                
                    if cornermatch:
                        elem=[]
                        elem.append(element)
                        for i in range(self.dictTypes[element][1]):
                            elem.append(cornermatch.group(i+1))
                        self.dictPlot[elem[1]]=elem
                         
                elif(p%2==1 and not typematch):
                    print("[lattice]: not possible to read line:", p)

        for element in self.dictPlot: 
            
            if self.dictPlot[element][0]=="monitor":
                x=[float(self.dictPlot[element][2]),float(self.dictPlot[element][2])]
                y=[0,0.005]
                self.ax1.plot(x,y,'k-')
                self.ax2.plot(x,y,'k-')
                
            elif self.dictPlot[element][0]=="dipole":            
                x=([float(self.dictPlot[element][2]),float(self.dictPlot[element][2]),
	               float(self.dictPlot[element][2])+float(self.dictPlot[element][3]),
	               float(self.dictPlot[element][2])+float(self.dictPlot[element][3])])
	            
	            y=[float(dictPlot[element][5])/2000+.003,float(self.dictPlot[element][5])/2000,
	               float(dictPlot[element][5])/2000,float(self.dictPlot[element][5])/2000+.003]
	            
	            self.ax1.plot(x,y,'r-')
	            self.ax2.plot(x,y,'r-')     
	            
	        elif self.dictPlot[element][0]=="quadrupole":
	            x=([float(self.dictPlot[element][2]),float(self.dictPlot[element][2]),
	               float(self.dictPlot[element][2])+float(self.dictPlot[element][3]),
	               float(self.dictPlot[element][2])+float(self.dictPlot[element][3])])
	            
	            y=[float(self.dictPlot[element][5])/2000+.003,float(self.dictPlot[element][5])/2000,
	               float(self.dictPlot[element][5])/2000,float(self.dictPlot[element][5])/2000+.003]
	            
	            self.ax1.plot(x,y,'g-')
	            self.ax2.plot(x,y,'g-')   
	            
	        
	        elif self.dictPlot[element][0]=="collimator":
	            x=[float(self.dictPlot[element][2]),float(self.dictPlot[element][2])]
	            y=[float(self.dictPlot[element][3])/2000,float(self.dictPlot[element][3])/2000+.003]
	            y2=[float(self.dictPlot[element][4])/2000,float(self.dictPlot[element][4])/2000+.003]
	            
	            self.ax1.plot(x,y,'b-')
	            self.ax2.plot(x,y2,'b-')
