##
# @file part_boxes.py
# @author Matthias Frey
# @date 16. Nov. 2016
# @brief Plot particles and grids in a plane

# 16. Nov. 2016, http://stackoverflow.com/questions/21445005/drawing-rectangle-with-border-only-in-matplotlib

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import colors
import sys
import numpy as np
import argparse

## Grid plotter class (in x-y plane)
# file format:
# node, level xlo   xhi  ylo   yhi  zlo   zhi
# {0}>  0     -1    1    -1    1    -1    1 
# {0}>  1     -0.5  0.5  -0.5  0.5  -0.5  0.5 
# {0}>  2     -0.25 0.25 -0.25 0.25 -0.25 0.25 
class Grids:
    
    ##
    def __init__(self):
        pass
    
    ## Read in a grid file
    # @param filename is the absolute path and name of file
    def read(self, filename):
        node, \
        self._level, \
        self._xlo, \
        self._xhi, \
        self._ylo, \
        self._yhi, \
        self._zlo, \
        self._zhi = np.loadtxt(filename,
                               unpack=True,
                               dtype={'names': ('node',
                                                'level',
                                                'xlo',
                                                'xhi',
                                                'ylo',
                                                'yhi',
                                                'zlo',
                                                'zhi'),
                                      'formats': ('|S15',
                                                  np.int,
                                                  np.float,
                                                  np.float,
                                                  np.float,
                                                  np.float,
                                                  np.float,
                                                  np.float)
                                      }
                               )
        
        # if scalar --> len() and max() do not work. (Error: iteration over 0-d array)
        # grids: grey to black (the higher the level the darker)
        if np.ndim(self._level) == 0:
            nLevel = self._level + 1
        else:
            nLevel = max(self._level) + 1
        ds = 1.0 / nLevel
        self._colors = []
        for i in range(nLevel):
            self._colors.append((0.9 - i * ds, 0.9 - i * ds, 0.9 - i * ds))
    
    ## Plot all grids on all levels
    # @param ax is the axis to plot on
    # @param plane is either x-y, x-z or y-z
    #        specified by 0, 1, or 2
    def plot(self, ax, plane):
        
        if np.ndim(self._level) == 0:
            l = 0
        else:
            l = len(self._level)
        
        for i in range(0, l):
            if plane == 0:
                self._add(self._xlo[i],
                          self._ylo[i],
                          self._xhi[i],
                          self._yhi[i],
                          ax,
                          self._colors[ self._level[i] ]
                          )
            elif plane == 1:
                self._add(self._xlo[i],
                          self._zlo[i],
                          self._xhi[i],
                          self._zhi[i],
                          ax,
                          self._colors[ self._level[i] ]
                          )
            else:
                self._add(self._ylo[i],
                          self._zlo[i],
                          self._yhi[i],
                          self._zhi[i],
                          ax,
                          self._colors[ self._level[i] ]
                          )
    
    ## Add one grid (called in self.plot)
    # @param x1 is the bottom horizontal value
    # @param y1 is the bottom vertical value
    # @param x2 is the upper horizontal value
    # @param y2 is the upper vertical value
    # @param ax is the axis to plot on
    # @param col is the color that depends on level
    def _add(self, x1, y1, x2, y2, ax, col):
        ax.add_patch(Rectangle((x1, y1),
                     x2 - x1,
                     y2 - y1,
                     alpha=1,
                     facecolor='none',
                     fill=None,
                     edgecolor=col,
                     linewidth=1.0)
        )

# Particle plotter class
class Particles:
    
    ##
    def __init(self):
        pass
    
    ## Read in a grid file
    # @param filename is the absolute path and name of file
    def read(self, filename):
        node, \
        self._xcoord, \
        self._ycoord, \
        self._zcoord, \
        self._pxcoord, \
        self._pycoord, \
        self._pzcoord = np.loadtxt(filename,
                                   unpack=True,
                                   dtype={'names': ('node',
                                                    'xcoord',
                                                    'ycoord',
                                                    'zcoord',
                                                    'pxcoord',
                                                    'pycoord',
                                                    'pzcoord'),
                                          'formats': ('|S15',
                                                      np.float,
                                                      np.float,
                                                      np.float,
                                                      np.float,
                                                      np.float,
                                                      np.float)
                                          }
                                   )
        print ( '#Particles: ', len(self._xcoord) )
    
    ## Plot all grids on all levels
    # @param ax is the axis to plot on
    # @param var1 first variable to plot ('x', 'y', 'z', 'px', 'py' or 'pz')
    # @param var2 second variable to plot ('x', 'y', 'z', 'px', 'py' or 'pz')
    def plot(self, ax, var1, var2):
        
        xvar, xlab = self._getArray(var1)
        yvar, ylab = self._getArray(var2)
        
        # 3. Dec. 2016,
        # http://stackoverflow.com/questions/17819502/how-can-you-put-a-matplotlib-artist-in-the-background-to-overlay-a-plot-on-top
        ax.scatter(xvar, yvar, s=1, marker='.', color='gray', zorder=0)
        ax.set_xlabel(xlab, fontsize=18)
        ax.set_ylabel(ylab, fontsize=18)
    
        
    ##
    # @returns the data of one variable 'x', 'y', 'z', 'px', 'py' or 'pz') and its label
    def _getArray(self, var):
        vlab = ''
        vcoord = []
        
        if var == 'x':
            vcoord = self._xcoord
            vlab = 'x [m]'
        elif var == 'y':
            vcoord = self._ycoord
            vlab = 'y [m]'
        elif var == 'z':
            vcoord = self._zcoord
            vlab = 'z [m]'
        elif var == 'px':
            vcoord = self._pxcoord
            vlab = 'px []'
        elif var == 'py':
            vcoord = self._pycoord
            vlab = 'py []'
        elif var == 'pz':
            vcoord = self._pzcoord
            vlab = 'pz []'
        return vcoord, vlab


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Visualization of particles and grids.')
    parser.add_argument('-d', '--directory', help='directory to files', default='.', type=str, nargs=1)
    parser.add_argument('-s', '--step', help='step file in directory', default=0, type=int, nargs=1)
    parser.add_argument('--xlim', help='horizontal boundary', type=float, nargs=2,
                        action='append')
    parser.add_argument('--ylim', help='vertical boundary', type=float, nargs=2,
                        action='append')
    parser.add_argument('--zlim', help='longitudinal boundary', type=float, nargs=2,
                        action='append')
    parser.add_argument('--pxlim', help='horizontal boundary', type=float, nargs=2,
                        action='append')
    parser.add_argument('--pylim', help='vertical boundary', type=float, nargs=2,
                        action='append')
    parser.add_argument('--pzlim', help='longitudinal boundary', type=float, nargs=2,
                        action='append')
    
    
    args = parser.parse_args()
    
    directory  = args.directory[0]
    step       = args.step[0]
    xlim       = args.xlim[0]
    ylim       = args.ylim[0]
    zlim       = args.zlim[0]
    pxlim      = args.pxlim[0]
    pylim      = args.pylim[0]
    pzlim      = args.pzlim[0]
    
    print ("Directory: ", directory)
    print ("Step:      ", step)
    print ("xlim:      ", xlim)
    print ("ylim:      ", ylim)
    print ("zlim:      ", zlim)
    print ("pxlim:     ", pxlim)
    print ("pylim:     ", pylim)
    print ("pzlim:     ", pzlim)
    
    particles = Particles()
    particles.read(directory + "pyplot_particles_" + str(step) + ".dat")

    grids = Grids()
    grids.read(directory + "pyplot_grids_" + str(step) + ".dat")
    
    
    plt.figure()
    plt.xlim(xlim)
    plt.ylim(ylim)
    particles.plot(plt.gca(), 'x', 'y')
    grids.plot(plt.gca(), 0)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_x_y_step-' + str(step) + '.png', bbox_inches='tight')
    
    plt.figure()
    plt.xlim(xlim)
    plt.ylim(zlim)
    particles.plot(plt.gca(), 'x', 'z')
    grids.plot(plt.gca(), 1)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_x_z_step-' + str(step) + '.png', bbox_inches='tight')
    
    plt.figure()
    plt.xlim(ylim)
    plt.ylim(zlim)
    particles.plot(plt.gca(), 'y', 'z')
    grids.plot(plt.gca(), 2)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_y_z_step-' + str(step) + '.png', bbox_inches='tight')
    
    plt.figure()
    plt.xlim(xlim)
    plt.ylim(pxlim)
    particles.plot(plt.gca(), 'x', 'px')
    grids.plot(plt.gca(), 2)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_x_px_step-' + str(step) + '.png', bbox_inches='tight')
    
    plt.figure()
    plt.xlim(ylim)
    plt.ylim(pylim)
    particles.plot(plt.gca(), 'y', 'py')
    grids.plot(plt.gca(), 2)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_y_py_step-' + str(step) + '.png', bbox_inches='tight')
    
    plt.figure()
    plt.xlim(zlim)
    plt.ylim(pzlim)
    particles.plot(plt.gca(), 'z', 'pz')
    grids.plot(plt.gca(), 2)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.savefig('ParticlePlot_z_pz_step-' + str(step) + '.png', bbox_inches='tight')
