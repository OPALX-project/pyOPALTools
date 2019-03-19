##
# @author Matthias Frey
# @date March 2018
#

import yt
import matplotlib.pyplot as plt
import numpy as np

class AmrOpal:
    """
    Plotter class for AMR data comming from OPAL.
    """
    
    def __init__(self):
        # dataset
        self.ds = ''
    
    
    def load_file(self, dirname, showme=False):
        """
        dirname (list)  directory name that contains a Header file and Level_x
                        (x = 0, 1, 2, ...) directories.
        showme  (str)   print fields and derived fields in dataset
        """
        self.ds = yt.load(dirname, dataset_type='boxlib_opal')
        
        self.ds.print_stats()
        
        if showme:
            print ( )
            print ("Field list:")
            for field in self.ds.field_list:
                print ( '    ', field )
            
            print ( )
            print ("Derived field list:")
            derived_field_list = self.ds.derived_field_list
            for dfield in self.ds.derived_field_list:
                print ( '    ', dfield )
    
        
    def line_plot(self, axis, field, **kwargs):
        """
        Plot a line plot of 3D data along an axis
        
        Parameters
        ----------
        axis    (str)   take a line cut along this axis
                        ('x', 'y', 'z')
        unit    (str)   of y-axis
        figsize=(12, 9) size of the figure
        dpi     (int)  resolution
        """
        
        if not self.ds:
            raise RuntimeError("AmrOpal.slice_plot: No dataset")
        
        unit    = kwargs.pop("unit", None)
        figsize = kwargs.pop('figsize', (12, 9))
        dpi     = kwargs.pop('dpi', None)
        
        
        # 27. May 2018
        # http://yt-project.org/doc/visualizing/manual_plotting.html
        cut1 = 1
        cut2 = 2
        
        ax = 0
        if axis == 'y':
            ax = 1
            cut1 = 0
            cut2 = 2
        elif axis == 'z':
            ax = 2
            cut1 = 0
            cut2 = 1
        elif not axis == 'x':
            raise RuntimeError("AmrOpal.line_plot: Use either 'x', 'y' or 'z' axis")
        
        c = self.ds.find_max(field)[1]
        ray = self.ds.ortho_ray(ax, (c[cut1], c[cut2]))
        
        srt = np.argsort(ray[axis])
        
        plt.plot(np.array(ray[axis][srt]),
                 np.array(ray[field][srt]), **kwargs)
        plt.ylabel(field + ' (' + unit + ')')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.xlabel(axis)
        
        return plt
    
    
    def slice_plot(self, normal, field, **kwargs):
        """
        Plot a slice through 3D data
        
        Parameters
        ----------
        normal (str)        is the direction 'x', 'y' or 'z' (normal)
        field  (str)        to plot
        unit   (str)        the data should be converted to
                            (otherwise it takes the default given by the data)
        zoom (float)        is the zoom factor (default: 1, i.e. no zoom)
        color   (str)       is the color for the time stamp and scale annotation
        origin  (str)       location of the origin of the plot coordinate system
        """
        
        unit              = kwargs.get("unit", None)
        zoom              = kwargs.get("zoom", 1.0)
        color             = kwargs.get("color", 'white')
        origin            = kwargs.get("origin", 'native')
        overlay_particles = kwargs.get("overlay_particles", False)
        time              = kwargs.get("time", True)
        gridcmap          = kwargs.get("gridcmap", 'B-W LINEAR_r')
        grids             = kwargs.get("grids", True)
            
        if not self.ds:
            raise RuntimeError("AmrOpal.slice_plot: No dataset")
        
        slc = yt.SlicePlot(self.ds, normal=normal,
                           fields=field, origin=origin)
        
        if unit is not None:
            slc.set_unit(field, unit)
        
        slc.zoom(zoom)
        
        if time:
            slc.annotate_timestamp(corner='upper_left', redshift=False, draw_inset_box=True)
        
        slc.annotate_scale(corner='upper_right', size_bar_args={'color':color})
        
        if overlay_particles:
            slc.annotate_particles(1.0)
        
        if grids:
            slc.annotate_grids(cmap=gridcmap)
        
        return slc
    
    
    def projection_plot(self, axis, field, **kwargs):
        """
        Plot a projection of 3D data
        
        Parameters
        ----------
        axis (str)          is the direction 'x', 'y' or 'z'
        field  (str)        to plot
        unit   (str)        the data should be converted to
                            (otherwise it takes the default given by the data)
        zoom (float)        is the zoom factor (default: 1, i.e. no zoom)
        color   (str)       is the color for the time stamp and scale annotation
        origin  (str)       location of the origin of the plot coordinate system
        method  (str)       method of projection ('mip', 'sum', 'integrate')
                            'mip':  maximum of field in the line of sight
                            'sum':  summation of the field along the given axis
                            'integrate': integrate the requested field along the line of sight
        """
        
        unit    = kwargs.get("unit", None)
        zoom    = kwargs.get("zoom", 1.0)
        color   = kwargs.get("color", 'white')
        origin  = kwargs.get("origin", 'native')
        method  = kwargs.get("method", 'mip')
        overlay_particles = kwargs.get("overlay_particles", False)
        time    = kwargs.get("time", True)
        gridcmap= kwargs.get("gridcmap", 'B-W LINEAR_r')
        grids   = kwargs.get("grids", True)
            
        if not self.ds:
            raise RuntimeError("AmrOpal.slice_plot: No dataset")
        
        
        slc = yt.ProjectionPlot(self.ds, axis, fields=field,
                                origin=origin, method=method)
        
        if unit is not None:
            slc.set_unit(field, unit)
    
        slc.zoom(zoom)
        
        if overlay_particles:
            slc.annotate_particles(1.0)
        
        if grids:
            slc.annotate_grids(cmap=gridcmap)
        
        if time:
            slc.annotate_timestamp(corner='upper_left', redshift=False, draw_inset_box=True)
        
        slc.annotate_scale(corner='upper_right', size_bar_args={'color':color})
        
        return slc
    
    
    def particle_plot(self, x_field, y_field, z_field=None, **kwargs):
        """
        Plot particle phase spaces etc of 3D data
        
        10. March 2018
        http://yt-project.org/doc/reference/api/yt.visualization.particle_plots.html#yt.visualization.particle_plots.ParticlePlot
        
        Parameters
        ----------
        x_field       (str)   particle field plotted on x-axis
        y_field       (str)   particle field plotted on y-axis
        z_field=None  (str)   field to be displayed on the colorbar
        """
        
        x_unit   = kwargs.get('x_unit', None)
        y_unit   = kwargs.get('y_unit', None)
        z_unit   = kwargs.get('z_unit', None)
        z_log    = kwargs.get('z_log', True)
        color    = kwargs.get('color', 'b')
        #origin   = kwargs.get('origin', 'native')
        fontsize = kwargs.get('fontsize', 16)
        deposit  = kwargs.get("deposition", 'ngp') # or 'cic'
        
        pp = yt.ParticlePlot(self.ds, x_field, y_field, z_field,
                             fontsize=fontsize, deposition=deposit) #, origin=origin)
        
        
        if x_unit:
            pp.set_unit(x_field, x_unit)
            
        if y_unit:
            pp.set_unit(y_field, y_unit)    
        
        if z_unit:
            #pp.set_cmap(z_field, 'RdBu')
            pp.set_log(z_field, z_log)
            #pp.set_zlim(z_field, zmin=-1e5, zmax=1e5)
            pp.set_unit(z_field, z_unit)
        
        return pp
    
    
    def particle_phase_space_plot(self, axis, **kwargs):
        """
        Plot particle phase spaces etc of 3D data
        
        10. March 2018
        http://yt-project.org/doc/reference/api/yt.visualization.particle_plots.html#yt.visualization.particle_plots.ParticlePlot
        
        Parameters
        ----------
        axis    (str)   'x', 'y' or 'z'
        """
        
        coordinate_unit = kwargs.get('coordinate_unit', None)
        momentum_unit   = kwargs.get('momentum_unit', None)
        color           = kwargs.get('color', 'b')
        deposition      = kwargs.get('deposition', 'ngp') # or 'cic'
        fontsize        = kwargs.get('fontsize', 16)
        
        coordinate = 'particle_position_'
        momentum   = 'particle_momentum_'
        
        if axis not in ['x', 'y', 'z']:
            raise RuntimeError("Phase space should be either 'x', 'y' or 'z'.")
        
        coordinate += axis
        momentum += axis
        
        pp = yt.ParticlePlot(self.ds, coordinate, momentum,
                             fontsize=fontsize,
                             deposition=deposition)
        
        if coordinate_unit:
            pp.set_unit(coordinate, coordinate_unit)
            
        if momentum_unit:
            pp.set_unit(momentum, momentum_unit)
        
        return pp
