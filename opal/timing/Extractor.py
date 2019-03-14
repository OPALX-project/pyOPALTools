##
# @author Matthias Frey
# @date July 2017
#

from opal.timing.Timing import Timing as timing
import os
import re

class Extractor:
    """
    Allows to collect all timing results from a
    directory or just a single specific OPAL output
    file.
    
    
    
    """
    
    def __init__(self):
        # bold red
        self._ecol = '\033[01;31m'
        self._files = []
    
    
    def collect(self, append = False, **kwargs):
        """
        Collect all files a timing should be extracted.
        
        Parameters
        ----------
        append (bool)   found files to list
        kwargs (dict)
            - path      directory to files
            - ext       file extension
                        if contains a '*' as last character
                        it finds all files with given string
                        (requires path to be set)
            - filename  if a specific file is checked
        
            
        Returns
        -------
        None
        
        References
        ----------
        None
        
        Examples
        --------
        None
        """
        
        path = ''
        if 'path' in kwargs:
            path = kwargs.get('path')
        
        fname = ''
        if 'filename' in kwargs:
            fname = kwargs.get('filename')
        
        ext = ''
        if 'ext' in kwargs:
            ext = kwargs.get('ext')
        
        if ext and not path:
            raise SyntaxError(self._ecol + \
                'Path required if file extension matching.' + self._ecol)
        
        files = []
        
        if ext and not fname:
            for f in os.listdir(path):
                if '*' in ext:
                    match = re.match('(.*\\' + ext[:-1] + '.*)', f)
                    if match:
                        files.append( path + '/' + match.group() )
                elif f.endswith(ext):
                    files.append( path + '/' + f )
        elif os.path.isfile(fname) and not ext:
            files.append( fname )
        else:
            raise SyntaxError(self._ecol + \
                'Specify either filename or file extension.' + self._ecol)
        
        
        if len(files) == 0:
            msg = ''
            for key, val in kwargs.iteritems():
                msg += '\t' + key + ': ' + val + '\n'
            
            raise RuntimeError(self._ecol + \
                'No files found with given arguments: \n' + msg + self._ecol)
        
        print ( 'Found ' + str(len(files)) + ' files.')
        
        if not append:
            self._files = []
        
        self._files += files
    
    
    def getFiles(self):
        """
        Returns
        -------
        all collected files
        """
        return self._files
    
    
    def write(self, pathname = './', filetype='ASCII'):
        """
        Extract all timings and write files
        """
        tt = timing.Timing()
        for f in self._files:
            # 14. July 2017
            # https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python/
            ext = os.path.splitext(f)[1]
            tt.read_output_file(f)
            f = f.replace(ext, '-timing.dat')
            tt.write(pathname + '/' + os.path.basename(f), filetype)
    
    
    def extract(self, filename):
        """
        Returns
        -------
        the timing data
        """
        tt = timing.Timing()
        tt.read_output_file(filename)
        return tt.getTiming()
    
