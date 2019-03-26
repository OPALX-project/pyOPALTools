# Author:   Matthias Frey
# Date:     March 2018 - 2019

from opal.datasets.SDDSDatasetBase import *

class StatDataset(SDDSDatasetBase):
    
    def __init__(self, directory, fname):
        vmapper = {
            'time':         't',
            'position':     's',
            '#particles':   'numParticles',
            'rms_z':        'rms_s',
            'rms_pz':       'rms_ps',
            'emit_z':       'emit_s',
            'mean_z':       'mean_s',
            'max_z':        'max_s',
        }
        
        lmapper  = {
            'rms_x':    r'$\sigma_x$',
            'rms_y':    r'$\sigma_y$',
            'rms_z':    r'$\sigma_z$',
            'rms_px':   r'$\sigma_{px}$',
            'rms_py':   r'$\sigma_{py}$',
            'rms_pz':   r'$\sigma_{pz}$',
            'emit_x':   r'$\varepsilon_x$',
            'emit_y':   r'$\varepsilon_y$',
            'emit_z':   r'$\varepsilon_z$',
            'mean_x':   r'$\mu_x$',
            'mean_y':   r'$\mu_y$',
            'mean_z':   r'$\mu_z$',
            'ref_x':    r'$x$ coordinate of reference particle',
            'ref_y':    r'$y$ coordinate of reference particle',
            'ref_z':    r'$z$ coordinate of reference particle',
            'ref_px':   r'$x$ momentum of reference particle',
            'ref_py':   r'$y$ momentum of reference particle',
            'ref_pz':   r'$z$ momentum of reference particle',
            'max_x':    r'max. beamsize in $x$',
            'max_y':    r'max. beamsize in $y$',
            'max_z':    r'max. beamsize in $z$',
            'xpx':      r'correlation $x p_x$',
            'ypy':      r'correlation $y p_y$',
            'zpz':      r'correlation $z p_z$',
            'Dx':       r'dispersion in $x$',
            'DDx':      r'derivative of dispersion in $x$',
            'Dy':       r'dispersion in $y$',
            'DDy':      r'derivative of dispersion in $y$',
            'Bx_ref':   r'$B_x$-field component of ref. particle',
            'By_ref':   r'$B_y$-field component of ref. particle',
            'Bz_ref':   r'$B_z$-field component of ref. particle',
            'Ex_ref':   r'$E_x$-field component of ref. particle',
            'Ey_ref':   r'$E_y$-field component of ref. particle',
            'Ez_ref':   r'$E_z$-field component of ref. particle',
            'dE':       'energy spread of the beam',
            'dt':       'time step size',
            'halo_x':   r'$h_x$',
            'halo_y':   r'$h_y$',
            'halo_z':   r'$h_z$'
        }
        
        umapper = [
            'rms_x',
            'rms_y',
            'rms_z',
            'time',
            'position',
            's',
            'energy',
            'emit_x',
            'emit_y',
            'emit_z',
            'mean_x',
            'mean_y',
            'mean_z',
            'ref_x',
            'ref_y',
            'ref_z',
            'max_x',
            'max_y',
            'max_z',
            'Dx',
            'Dy',
            'Bx_ref',
            'By_ref',
            'Bz_ref',
            'Ex_ref',
            'Ey_ref',
            'Ez_ref',
            'dE',
            'dt'
        ]
        
        super(StatDataset, self).__init__(directory, fname,
                                          variable_mapper=vmapper,
                                          label_mapper=lmapper,
                                          unit_label_mapper=umapper,
                                          dataset_type='Statistic')
