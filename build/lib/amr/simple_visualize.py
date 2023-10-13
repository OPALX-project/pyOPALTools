# Copyright (c) 2018, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

import os
import argparse

from amr import AmrOpal

try:
    parser = argparse.ArgumentParser(description='Visualize AmrOpal grid data.')
    parser.add_argument('--zoom',
                        help='zoom factor of images (default: 1)',
                        default=1,
                        type=float,
                        nargs='?',
                        const=1)
    
    parser.add_argument('--pltfile',
                        help='plot file',
                        type=str)
    
    args = parser.parse_args()
    
    zoom = args.zoom
    
    pltfile = args.pltfile
    
    ao = AmrOpal()
    
    ao.load_file(pltfile)
    
    ao.slice_plot(normal='z', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.slice_plot(normal='y', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.slice_plot(normal='x', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.projection_plot(axis='x', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.projection_plot(axis='y', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.projection_plot(axis='z', field='rho', unit='C/m**3', zoom=zoom, color='gray')
    
    ao.slice_plot(normal='z', field='Ex', unit='V/m', zoom=zoom)
    
    ao.slice_plot(normal='z', field='Ey', unit='V/m', zoom=zoom)
    
    ao.slice_plot(normal='x', field='Ez', unit='V/m', zoom=zoom)
    
    ao.slice_plot(normal='z', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.slice_plot(normal='y', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.slice_plot(normal='x', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.projection_plot(axis='z', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.projection_plot(axis='y', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.projection_plot(axis='x', field='electrostatic_potential', unit='V', zoom=zoom)
    
    ao.line_plot(axis='x', field='electrostatic_potential', unit='V')
    ao.line_plot(axis='y', field='electrostatic_potential', unit='V')
    ao.line_plot(axis='z', field='electrostatic_potential', unit='V')
    
    ao.line_plot(axis='z', field='Ex', unit='V/m')
    ao.line_plot(axis='z', field='Ey', unit='V/m')
    ao.line_plot(axis='x', field='Ez', unit='V/m')
    
except IOError as e:
    print (e.strerror)
