# Author:   Matthias Frey
# Date:     25. May 2018

import os
import fileinput
import shutil

class JobSubmitter:
    
    def __init__(sim_dirs, template, pair, cmd):
        """
        Instantiation.
        
        Parameters
        ----------
        sim_dirs    (list)  all simulation directories
        template    (str)   batch script template file, entries
                            to be replaced start and end with an
                            underscore '_'
        pair        (dict)  keys are strings that are replaced
                            in the template file (keys do not have
                            '_') with corresponding value.
        cmd         (str)   batch submit command, e.g. sbatch for SLURM
        
        
        Note
        ----
        1. Create batch scripts with JobSubmitter.write_run_file function
        2. Submit jobs with JobSubmitter.submit() function
        """
        self._sim_dirs = []
        
        for sdir in sim_dirs:
            tmp = os.path.abspath(sdir)
            if not os.path.isdir(tmp):
                raise IOError( "Error: Directory '" + tmp + "' doesn't exist." )
            self._sim_dirs.append( tmp )
        
        self._pair = pair
        
        template = os.path.abspath(template)
        if not os.path.isfile(template):
            raise IOError( "Error: Template file '" + template + "' doesn't exist." )
        
        self._template = template
        self._cmd = cmd
        self._runfile = 'run_job.sh'
    
    
    def submit():
        """
        Submit all jobs.
        """
        for sdir in self._sim_dirs:
            os.chdir(sdir)
            
            tmp = os.path.join(sdir, self._runfile)
            if not os.path.isfile(tmp):
                raise IOError( "Error: Batch script '" + tmp + "' doesn't exist.")
            os.system(self._cmd + ' ' + self._runfile)
    
    
    def write_run_file(self):
        """
        Create a 'run_job.sh' file for each simulation.
        """
        for sdir in self._sim_dirs:
            shutil.copy(self._template, sdir)
            
            fname = os.path.basename(self._template)
            fname = os.path.join(sdir, fname)
            with fileinput.FileInput(fname, inplace=True) as file:
                for line in file:
                    for key, val in self._pair.items()
                        print(line.replace('_' + key + '_', val), end='')
