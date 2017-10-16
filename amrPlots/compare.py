##
# @file compare.py
# @author Matthias Frey
# @date 16. October 2017
# @version 1.0
# 
# @pre Python >= 2.7
# @details Compare two line plots.

import os
import yt
import argparse
import numpy
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

try:
    parser = argparse.ArgumentParser(description='Compare BoxLib grid data.')
    
    parser.add_argument('--pltfile1',
                        help='plot file',
                        type=str)
    
    parser.add_argument('--pltfile2',
                        help='plot file',
                        type=str)
    
    args = parser.parse_args()
    
    pltfile1 = args.pltfile1
    
    ds1 = yt.load(pltfile1, dataset_type='boxlib_opal')
    
    
    pltfile2 = args.pltfile2
    
    ds2 = yt.load(pltfile2, dataset_type='boxlib_opal')
    
    
    ax = 0 # take a line cut along the x axis
    
    
    c1 = ds1.find_max('electrostatic_potential')[1]
    ray1 = ds1.ortho_ray(ax, c1)
    
    c2 = ds2.find_max('electrostatic_potential')[1]
    ray2 = ds2.ortho_ray(ax, c2)
    
    print ( 'center 1: ', c1 )
    print ( 'center 2: ', c2 )
    
    srt1 = numpy.argsort(ray1['x'])
    srt2 = numpy.argsort(ray2['x'])
    
    font_dict = {}
    font_dict.setdefault('family', 'stixgeneral')
    font_dict.setdefault('size', 18)
    FontProperties(**font_dict)
    
    plt.plot(numpy.array(ray1['x'][srt1]),
             numpy.array(ray1['electrostatic_potential'][srt1]))
    
    plt.plot(numpy.array(ray2['x'][srt2]),
             numpy.array(ray2['electrostatic_potential'][srt2]))
    
    plt.ylabel(r'$\rm{\Phi }$ (V)')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel('x-axis')
    plt.legend([os.path.basename(pltfile1), os.path.basename(pltfile2)])
    plt.savefig('line_plot_x_electrostatic_potential_comparison.png')
    
    
    plt.close()
    
    plt.plot(numpy.array(ray1['x'][srt1]),
             numpy.array(ray1['Ex'][srt1]))
    
    plt.plot(numpy.array(ray2['x'][srt2]),
             numpy.array(ray2['Ex'][srt2]))
    
    plt.ylabel(r'$\rm{E_x}$ (V/m)')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel('x-axis')
    plt.legend([os.path.basename(pltfile1), os.path.basename(pltfile2)])
    plt.savefig('line_plot_x_efield_comparison.png')
    
except IOError as e:
    print (e.strerror)
