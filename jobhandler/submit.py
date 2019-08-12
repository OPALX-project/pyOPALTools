# Author:   Matthias Frey
# Date:     25. May 2018

import os
import fileinput
import shutil
import re

class JobSubmitter:
    
    def __init__(self, sim_dirs, template, pair, cmd, additions=[]):
        """
        Instantiation.
        
        Parameters
        ----------
        sim_dirs    (list)  all simulation directories
        template    (str)   batch script template file, entries
                            to be replaced start and end with an
                            at sign '@'
        pair        (dict)  keys are strings that are replaced
                            in the template file (keys do not have
                            '@') with corresponding value.
        cmd         (str)   batch submit command, e.g. sbatch for SLURM
        additions   ([str]) additional commands like 'source', export
                            that should be added to the file. These will be
                            prepended
        
        
        Note
        ----
        1. Submit jobs with JobSubmitter.submit() function
        """
        self._sim_dirs = []

        if not isinstance(sim_dirs, list):
            sim_dirs = [sim_dirs]

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
        
        self._write_run_file(additions)
    
    
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
    
    
    def _write_run_file(self, additions):
        """
        Create a 'run_job.sh' file for each simulation.
        """
        pattern = r'@(.*?)@'
        
        if additions:
            for i, add in enumerate(additions):
                additions[i] = add + '\n'
            additions[-1] += '\n'

        for sdir in self._sim_dirs:
            shutil.copy(self._template, sdir)
            
            fname = os.path.basename(self._template)
            fname = os.path.join(sdir, fname)

            if additions:
                with open(fname, "r") as f:
                    lines = []
                    for line in f:
                        lines.append(line)
                # 12. March 2019
                # https://stackoverflow.com/questions/2170900/get-first-list-index-containing-sub-string
                index = [idx for idx, s in enumerate(lines) if not '#' in s][0]
                lines = lines[0:index] + additions + lines[index:]
                ftmp = fname + '.tmp'
                with open(ftmp, "w") as f:
                    for a in lines:
                        f.write(a)
                os.rename(ftmp, fname)

            with fileinput.FileInput(fname, inplace=True) as f:
                for line in f:
                    obj = re.findall(pattern, line)
                    if obj:
                        for key in obj:
                            if key in self._pair:
                                val = self._pair[key]
                                line = line.replace('@' + key + '@', str(val))
                    print(line, end='')
