# Author:   Philippe Ganz
# Date:     March 2018

import re

class LatticeParser:

    def __init__(self):
        """Constructor.
        """
        self._pattern_quadrupole=re.compile(r'''QUADRUPOLE \n
                                            ''',re.VERBOSE|re.UNICODE)
        self._pattern_monitor=re.compile(r'''MONITOR \n
                                         ''',re.VERBOSE|re.UNICODE)
        self._pattern_collimator=re.compile(r'''COLLIMATOR \n
                                            ''',re.VERBOSE|re.UNICODE)
        self._pattern_dipole=re.compile(r'''DIPOLE \n
                                        ''',re.VERBOSE|re.UNICODE)
        self._pattern_corner=re.compile(r'''(?P<name>[A-Z,0-9]*) [\s]+
                                        (?P<one>[0-9]+ [.]? [0-9]*) [\s]*
                                        ((?P<two>[0-9]+ [.]? [0-9]*) [\s]*)?
                                        ((?P<three>[0-9]+ [.]? [0-9]*) [\s]*)?
                                        (?P<four>[0-9]+ [.]? [0-9]*)? \s* \n
                                        ''',re.VERBOSE|re.UNICODE)
        self._dictTypes= {
            "monitor": [self._pattern_monitor, 2, 'k-'],
            "collimator":[self._pattern_collimator, 4, 'k-'],
            "dipole": [self._pattern_dipole, 5, 'b-'],
            "quadrupole":[self._pattern_quadrupole, 5, 'r-'],
        }


    def plot(self, lfile, fig, ax1, ax2):

        dictPlot={}

        m2mm = 1000.0
        diameter2radius = 2.0

        rectangle_edge = 0.003

        scale = m2mm * diameter2radius

        with open(lfile, 'r') as lattice:
            for p, line in enumerate(lattice):
                if p%2==0:
                    for eltype in self._dictTypes:
                        typematch=self._dictTypes[eltype][0].match(line)
                        if typematch:
                            element=eltype
                            break

                if p%2==1 and typematch:
                    cornermatch= self._pattern_corner.match(line)

                    if cornermatch:
                        elem=[]
                        elem.append(element)
                        for i in range(self._dictTypes[element][1]):
                            elem.append(cornermatch.group(i+1))
                        dictPlot[elem[1]]=elem

                elif(p%2==1 and not typematch):
                    print("[lattice]: not possible to read line:", p)

        for element in dictPlot:

            if dictPlot[element][0]=="monitor":
                x=[float(dictPlot[element][2]),float(dictPlot[element][2])]
                y=[0,0.005]
                ax1.plot(x,y,'k-')
                ax2.plot(x,y,'k-')

            elif dictPlot[element][0]=="dipole":
                 x=([float(dictPlot[element][2]),float(dictPlot[element][2]),
                   float(dictPlot[element][2])+float(dictPlot[element][3]),
                   float(dictPlot[element][2])+float(dictPlot[element][3])])

                 y=[float(dictPlot[element][5])/scale+rectangle_edge,float(dictPlot[element][5])/scale,
                   float(dictPlot[element][5])/scale,float(dictPlot[element][5])/scale+rectangle_edge]

                 ax1.plot(x,y,'r-')
                 ax2.plot(x,y,'r-')

            elif dictPlot[element][0]=="quadrupole":

                x=([float(dictPlot[element][2]),float(dictPlot[element][2]),
                   float(dictPlot[element][2])+float(dictPlot[element][3]),
                   float(dictPlot[element][2])+float(dictPlot[element][3])])

                y=[float(dictPlot[element][5])/scale+rectangle_edge,float(dictPlot[element][5])/scale,
                   float(dictPlot[element][5])/scale,float(dictPlot[element][5])/scale+rectangle_edge]

                ax1.plot(x,y,'g-')
                ax2.plot(x,y,'g-')


            elif dictPlot[element][0]=="collimator":
                x=[float(dictPlot[element][2]),float(dictPlot[element][2])]
                y=[float(dictPlot[element][3])/scale,float(dictPlot[element][3])/scale+rectangle_edge]
                y2=[float(dictPlot[element][4])/scale,float(dictPlot[element][4])/scale+rectangle_edge]

                ax1.plot(x,y,'b-')
                ax2.plot(x,y2,'b-')
