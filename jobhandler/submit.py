# Author:   Matthias Frey
# Date:     25. May 2018

import os
import fileinput
import shutil
import re

class JobSubmitter:
    
    def __init__(self, sim_dirs, template, pair, cmd):
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
        1. Submit jobs with JobSubmitter.submit() function
        """
        self._sim_dirs = []
        
        for sdir in sim_dirs:
            tmp = os.path.abspath(sdir)
            if not os.path.isdir(tmp):
                raise IOError( "Error: Directory '" + tmp + "' doesn't exist." )
            self._sim_dirs.append( tmp )
        self._pair = pair
        
        # expand environment variables
        template = os.path.expandvars(template)
        if not os.path.isabs(template):
            template = os.path.abspath(template)
        if not os.path.isfile(template):
            raise IOError( "Error: Template file '" + template + "' doesn't exist." )
        
        self._template = template
        self._cmd = cmd
        self._runfile = os.path.basename(template)
        
        self._write_run_file()
    
    
    def submit(self):
        """
        Submit all jobs.
        """
        for sdir in self._sim_dirs:
            os.chdir(sdir)
            
            tmp = os.path.join(sdir, self._runfile)
            if not os.path.isfile(tmp):
                raise IOError( "Error: Batch script '" + tmp + "' doesn't exist.")
            os.system(self._cmd + ' ' + self._runfile)
    
    
    def _write_run_file(self):
        """
        Create a 'run_job.sh' file for each simulation.
        """
        pattern = r'_(.*?)_'
        
        for sdir in self._sim_dirs:
            shutil.copy(self._template, sdir)
            
            fname = os.path.basename(self._template)
            fname = os.path.join(sdir, fname)
            with fileinput.FileInput(fname, inplace=True) as f:
                for line in f:
                    obj = re.findall(pattern, line)
                    if obj:
                        for key in obj:
                            if key in self._pair:
                                val = self._pair[key]
                                line = line.replace('_' + key + '_', str(val))
                    print(line, end='')
