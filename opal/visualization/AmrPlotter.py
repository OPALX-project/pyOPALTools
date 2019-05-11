from .BasePlotter import *
import numpy as np

class AmrPlotter(BasePlotter):
    
    def __init__(self):
        pass
    
    
    def line_plot(self, axis, field, **kwargs):
        """
        Plot a line plot of 3D data along an axis
        
        Parameters
        ----------
        axis    (str)           take a line cut along this axis
                                ('x', 'y', 'z')
        unit    (str)           of y-axis
        """
        unit    = kwargs.pop("unit", None)
        
        xvals, yvals = self.ds.get_ray_along(axis, field)
        
        plt.plot(xvals, yvals, **kwargs)
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
        import yt
        
        unit              = kwargs.pop("unit", None)
        zoom              = kwargs.pop("zoom", 1.0)
        color             = kwargs.pop("color", 'white')
        origin            = kwargs.pop("origin", 'native')
        overlay_particles = kwargs.pop("overlay_particles", False)
        time              = kwargs.pop("time", True)
        gridcmap          = kwargs.pop("gridcmap", 'B-W LINEAR_r')
        grids             = kwargs.pop("grids", True)
        
        slc = yt.SlicePlot(self.ds.real_ds, normal=normal,
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
        axis   (str)        is the direction 'x', 'y' or 'z'
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
        import yt
        
        unit    = kwargs.pop("unit", None)
        zoom    = kwargs.pop("zoom", 1.0)
        color   = kwargs.pop("color", 'white')
        origin  = kwargs.pop("origin", 'native')
        method  = kwargs.pop("method", 'sum')
        overlay_particles = kwargs.pop("overlay_particles", False)
        time    = kwargs.pop("time", True)
        gridcmap= kwargs.pop("gridcmap", 'B-W LINEAR_r')
        grids   = kwargs.pop("grids", True)
            
        slc = yt.ProjectionPlot(self.ds.real_ds, axis, fields=field,
                                origin=origin, method=method)
        
        if unit is not None:
            slc.set_unit(field, unit)
    
        slc.zoom(zoom)
        
        if overlay_particles:
            slc.annotate_particles(1.0)
        
        if grids:
            import matplotlib as mpl
            slc.annotate_grids(cmap=gridcmap, linewidth=mpl.rcParams['grid.linewidth'])
        
        if time:
            slc.annotate_timestamp(corner='upper_left', redshift=False, draw_inset_box=True)
        
        slc.annotate_scale(corner='lower_right', size_bar_args={'color':color})
        
        return slc


    def particle_plot(self, x_field, y_field, z_field=None, **kwargs):
        """
        Plot particle phase spaces etc of 3D data
        
        10. March 2018
        http://yt-project.org/doc/reference/api/yt.visualization.particle_plots.html#yt.visualization.particle_plots.ParticlePlot
        
        Parameters
        ----------
        x_field       (str)         particle field plotted on x-axis
        y_field       (str)         particle field plotted on y-axis
        z_field=None  (str)         field to be displayed on the colorbar
        """
        import yt
        
        x_unit   = kwargs.pop('x_unit', None)
        y_unit   = kwargs.pop('y_unit', None)
        z_unit   = kwargs.pop('z_unit', None)
        z_log    = kwargs.pop('z_log', True)
        color    = kwargs.pop('color', 'b')
        #origin   = kwargs.pop('origin', 'native')
        fontsize = kwargs.pop('fontsize', 16)
        deposit  = kwargs.pop("deposition", 'ngp') # or 'cic'
        
        pp = yt.ParticlePlot(self.ds.real_ds, x_field, y_field, z_field,
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
        axis    (str)           'x', 'y' or 'z'
        """
        import yt
        
        coordinate_unit = kwargs.pop('coordinate_unit', None)
        momentum_unit   = kwargs.pop('momentum_unit', None)
        color           = kwargs.pop('color', 'b')
        deposition      = kwargs.pop('deposition', 'ngp') # or 'cic'
        fontsize        = kwargs.pop('fontsize', 16)
        
        coordinate = 'particle_position_'
        momentum   = 'particle_momentum_'
        
        if axis not in ['x', 'y', 'z']:
            raise RuntimeError("Phase space should be either 'x', 'y' or 'z'.")
        
        coordinate += axis
        momentum += axis
        
        pp = yt.ParticlePlot(self.ds.real_ds, coordinate, momentum,
                             fontsize=fontsize,
                             deposition=deposition)
        
        if coordinate_unit:
            pp.set_unit(coordinate, coordinate_unit)
        
        if momentum_unit:
            pp.set_unit(momentum, momentum_unit)
        
        return pp
