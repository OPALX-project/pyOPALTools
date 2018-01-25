##
# @author Matthias Frey
# @date 2016 - 2017
#

import pickle as pickle
import pprint
import re


class Timing:

    """
    Read and write an Ippl timing file.
    
    Example:
    
    import Timing as timing
    
    time = timing.Timing()
    
    time.read_ippl_timing("/path/to/IpplTiming.dat")
    
    data = time.getTiming()
    
    print ( data )
    
    time.pie_plot('cpu avg'):
    
    
    Parameters
    ----------
    _data ([])  list of dictionaries
    
    Notes
    -----
    It stores the data in a list of dictionary
    where the main timing dictionary is
    
        main_dict = {'cpu tot':     [],
                     'wall tot':    [],
                     'what':        [],
                     'cores':       []}
        
    and the specialized timings are in stored in a
    dictionary with the structure
    
        special_dict = {'what':     [],
                        'cpu max':  [],
                        'wall max': [],
                        'cpu min':  [],
                        'wall min': [],
                        'cpu avg':  [],
                        'wall avg': []}
        
    The list of dictionaries looks then as follows:
        
        self._data = [main_dict,
                      special_dict_1,
                      ...,
                      special_dict_N]
    
    Examples
    --------
    None
    
    """

    def __init__(self):
        # list of dictionaries
        self._problem = {}
        self._data = []
        self._format = ['PICKLE',
                        'ASCII']
    
    
    def _init_data_structure(self):
        """
        This is the way the timing is stored
        
        Parameters
        ----------
        None
        
        Returns
        -------
        main_dict       the dictionary for the main timer
        special_dict    the dictionary for all other timers
        
        References
        ----------
        None
        
        Examples
        --------
        None
        """
        
        main_dict = {'cpu tot':     [],
                     'wall tot':    [],
                     'what':        [],
                     'cores':       []}
        
        special_dict = {'what':     [],
                        'cpu max':  [],
                        'wall max': [],
                        'cpu min':  [],
                        'wall min': [],
                        'cpu avg':  [],
                        'wall avg': []}
        return main_dict, special_dict
    
    
    def read_output_file(self, f):
        """
        Read in the timing results from an OPAL
        output file.
        
        Parameters
        ----------
        f (str) is the pathname (i.e. path + filename)
        
        Returns
        -------
        None
        
        References
        ----------
        None
        
        Examples
        --------
        None
        
        Notes
        -----
        Following format assumed:
        
        Timings{0}> -----------------------------------------------------------------
        Timings{0}>      Timing results for 32 nodes:
        Timings{0}> -----------------------------------------------------------------
        Timings{0}> mainTimer........... Wall tot =    326.192, CPU tot =     325.76
        Timings{0}> 
        Timings{0}> my awesome timer.... Wall max =          0, CPU max =          0
        Timings{0}>                      Wall avg =          0, CPU avg =          0
        Timings{0}>                      Wall min =          0, CPU min =          0
        Timings{0}>
        Timings{0}> super timer......... Wall max =    14.6091, CPU max =      14.52
        Timings{0}>                      Wall avg =    3.34291, CPU avg =    3.31844
        Timings{0}>                      Wall min =   0.007039, CPU min =          0
        Timings{0}>
        Timings{0}> best timer.......... Wall max =    33.4165, CPU max =      32.93
        Timings{0}>                      Wall avg =    23.0727, CPU avg =    22.8328
        Timings{0}>                      Wall min =     19.989, CPU min =      19.67
        Timings{0}>
        Timings{0}> -----------------------------------------------------------------
        """
        
        
        self._data = []
        
        main_dict, special_dict = self._init_data_structure()
        
        # 13. July 2017
        # https://stackoverflow.com/questions/2301789/read-a-file-in-reverse-order-using-python
        lines = []
        count = 0
        
        for line in reversed(open(f).readlines()):
            if "Timings" in line:
                lines.insert(0, line)
            else:
                break
        
        # we parse it the right order
        for line in lines:
            if "Timing results for" in line:
                    words = line.split()
                    main_dict['cores'] = words[4]
            
            elif "Wall tot" in line:
                # main timer
                main_dict['what'], \
                main_dict['wall tot'], \
                main_dict['cpu tot'] = self._parse_line(line, 'tot')
                self._data.append(dict(main_dict))
                
            elif "Wall max" in line:
                # special timer
                special_dict['what'], \
                special_dict['wall max'], \
                special_dict['cpu max'] = self._parse_line(line, 'max')
                count += 1
            elif "Wall min" in line:
                special_dict['wall min'], \
                special_dict['cpu min'] = self._parse_line(line, 'min')
                count += 1
            elif "Wall avg" in line:
                special_dict['wall avg'], \
                special_dict['cpu avg'] = self._parse_line(line, 'avg')
                count += 1
        
            if count == 3:
                count = 0
                self._data.append(dict(special_dict))
    
    
    def _parse_line(self, line, time):
        """
        Used in read_output_file() for getting the timing values
        
        Parameters
        ----------
        line (str)      to parse
        time (str)      'tot', 'avg', 'min' or 'max'
        
        Returns
        -------
        wall  (float)   time number
        cpu   (float)   time number
        timer (str)     timer name (only if time == 'max')
        
        References
        ----------
        None
        
        Examples
        --------
        None
        """
        
        pattern = ''
        
        if time == 'max' or time == 'tot':
            pattern = '.*> (.*) Wall ' + time + ' = (.*), CPU ' + time + ' = (.*)'
        elif time == 'min' or time == 'avg':
            pattern = '.*> .* Wall ' + time + ' = (.*), CPU ' + time + ' = (.*)'
        
        match = re.match(pattern, line)
        
        if time == 'max' or time == 'tot':
            timer = match.group(1).replace('.', '')
            wall  = float(match.group(2))
            cpu   = float(match.group(3))
            return timer,  wall, cpu
        else:
            wall = float(match.group(1))
            cpu  = float(match.group(2))
            return wall, cpu
    
    
    def read_ippl_timing(self, f):
        
        """
        Read in an Ippl timing file created by
        
        std::string filename = "myTiming.dat";
        Ippl:print(filename, problemSize);
        
        The problem size is optional.
        
        Parameters
        ----------
        f (str) is the pathname (i.e. path + filename)
        
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
        
        self._data = []
        
        main_dict, special_dict = self._init_data_structure()
        
        
        # obtain problem size parameter
        toSkip = 0
        with open(f) as ff:
            toSkip = self._problemsize(ff)
        
        
        with open(f) as ff:
            
            line = self._skip_lines(ff, toSkip)
            tag = self._order(line, 1)
            
            # get main timing
            line = self._skip_lines(ff, 1)
            
            # 25. Jan. 2018
            # https://stackoverflow.com/questions/12866631/python-split-a-string-with-at-least-2-whitespaces
            words = re.split(r'\s{2,}', line)
            
            if len(words) != 4:
                raise RuntimeError('Not able to parse main timing')
            
            # remove appending dots "..." of timing names
            main_dict['what']       = words[0].replace('.', '')
            main_dict['cores']      = words[tag['num nodes']].rstrip('\n')
            main_dict['cpu tot']    = float(words[tag['cpu tot']].rstrip('\n'))
            main_dict['wall tot']   = float(words[tag['wall tot']].rstrip('\n'))
            
            # we need to copy otherwise it overwrites the data
            self._data.append(dict(main_dict))
            
            # get special timings
            line = self._skip_lines(ff, 1)
            
            tag = self._order(line, 1)
            
            line = self._skip_lines(ff, 0)
            
            for line in ff:
                words = re.split(r'\s{2,}', line)
                special_dict['what']        = words[0].replace('.', '')
                special_dict['cpu max']     = float(words[tag['cpu max']].rstrip('\n'))
                special_dict['wall max']    = float(words[tag['wall max']].rstrip('\n'))
                special_dict['cpu min']     = float(words[tag['cpu min']].rstrip('\n'))
                special_dict['wall min']    = float(words[tag['wall min']].rstrip('\n'))
                special_dict['cpu avg']     = float(words[tag['cpu avg']].rstrip('\n'))
                special_dict['wall avg']    = float(words[tag['wall avg']].rstrip('\n'))
                
                # we need to copy otherwise it overwrites the data
                self._data.append(dict(special_dict))
    
    
    def getTiming(self):
        
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        the timing data
        
        Notes
        -----
        It is not checked if the container is empty.
        
        References
        ----------
        None
        """
        return self._data
    
    
    def getProblemSize(self):
        """
        Parameters
        ----------
        None
        
        Returns
        -------
        all problem specification in a dictionary
        
        Notes
        -----
        It is not checked if the container is empty.
        
        References
        ----------
        None
        """
        return self._problem
    
    
    def __str__(self):
        if not self._data:
            return 'There is no data loaded.'
        else:
            out = ''
            for dic in self._data:
                if ('mainTimer' == dic['what'] or 'main' == dic['what']) and 'cores' in dic:
                    out += "\t\t num Nodes    CPU tot   Wall tot\n"
                    out += "=" * 48 + "\n"
                    out += dic['what'] + "\t\t" + str(dic['cores']) + "    " + \
                        str(dic['cpu tot']) + "    " + str(dic['wall tot']) + "\n"
                    out += "\n\t\t\t CPU max\t Wall max\t CPU min\t Wall min\t CPU avg\t Wall avg\n"
                    out += "=" * 115 + "\n"
                else:
                    # 16. Jan. 2017
                    # http://stackoverflow.com/questions/20309255/how-to-pad-a-string-to-a-fixed-length-with-spaces-in-python
                    out += "{:<20}".format(dic['what']) + "\t"
                    out += "{:<10}".format(str(dic['cpu max'])) + "\t"
                    out += "{:<10}".format(str(dic['wall max'])) + "\t"
                    out += "{:<10}".format(str(dic['cpu min'])) + "\t"
                    out += "{:<10}".format(str(dic['wall min'])) + "\t"
                    out += "{:<10}".format(str(dic['cpu avg'])) + "\t"
                    out += "{:<10}".format(str(dic['wall avg']))
                    out += "\n"
            return out
    
    
    def read(self, pathname, info=False):
        
        """
        Parameters
        ----------
        pathname (str)      path + filename of pickle file
        info=False (bool)   print data when reading
        
        References
        ----------
        None
        
        Notes
        -----
        None
        
        Returns
        -------
        None
        """
        
        self._data = []
        
        with open(pathname, 'rb') as f:
            for data in self._load_pkl(f):
                self._data.append(data)
                if info:
                    pprint.pprint(data)
    
    
    def write(self, pathname, form = 'PICKLE', data = None):
        """
        Export a timing data in a specific format
        
        Parameters
        ----------
        pathname        (str)   path + name of the written file
        data            ([{}])  timing data
        form="PICKLE"   (str)   in which format to write
        
        Returns
        -------
        None
        
        Notes
        -----
        Throws an exception if the format is unknown or
        not available
        """
        
        if not data and not self._data:
            raise RuntimeError('No data available.')
        elif not data:
            data = self._data
        
        if form == self._format[0]:
            self._exportPickle(pathname, data)
        elif form == self._format[1]:
            self._exportAscii(pathname, data)
        else:
            raise RuntimeError('Not supported export format.')
    
    
    def _load_pkl(self, pkl_file):
        """
        Pickle file loading function
        
        Parameters
        ----------
        pkl_file    (str)   pickle timing file to load
        
        """
        
        # 14. Jan. 2017, http://stackoverflow.com/questions/18675863/load-data-from-python-pickle-file-in-a-loop
        try:
            while True:
                yield pickle.load(pkl_file)
        except EOFError:
            pass
    
    def _order(self, line, i):
        """
        Find the order of the tags, i.e. 'cpu min', etc.
        and fill dictionary.
        
        Parameters
        ----------
        line    (str) of file
        i       (int) start indexing
        
        Returns
        -------
        the a dictionary giving tag as key and
        occurrence as number.
        """
        
        line = line.lower()
        
        words = re.split(r'\s{2,}', line)
        
        order = {}
        for w in words:
            if w:
                order[w.strip('\n')] = i
                i += 1
        
        return order
    
    
    def _problemsize(self, ff):
        """
        Read the problemsize.
        
        Parameters
        ----------
        ff   (str)  the opened file
        n   (int)   the number of lines to skip
        
        Returns
        -------
        the number of read lines.
        
        """
        
        if not 'Problem size' in ff.readline():
            return 0
        
        line = ff.readline()
        
        nLines = 2
        
        pattern = '(.*):(.*)'
        
        self._problem = {}
        
        while not line.isspace():
            
            obj = re.match(pattern, line)
            
            if obj:
                self._problem[obj.group(1).lstrip()] = int(obj.group(2))
            
            line = ff.readline()
            nLines += 1
        
        return nLines
    
    
    def _skip_lines(self, f, n):
        """
        Skip n lines of the opened file f
        
        Parameters
        ----------
        f   (str)   the opened file
        n   (int)   the number of lines to skip
        
        Returns
        -------
        new line
        
        """
        
        for _ in range(n):
            next(f)
        
        return f.readline()
    
    def _exportPickle(self, pathname, data):
        """
        Write a binary pickle file
        
        Parameters
        ----------
        pathname    (str)   path + filename of written file
        data        ([{}])  timing data
        
        Notes
        -----
        If pathname has no extension the string ".pkl" is
        appended
        """
        
        if '.' not in pathname:
            pathname = pathname + ".pkl"
        
        f = open(pathname, 'wb')
        
        for dic in data:
            pickle.dump(dic, f)
        
        f.close()
    
    def _exportAscii(self, pathname, data):
        """
        Write a human readable file
        
        Parameters
        ----------
        pathname    (str)   path + filename of written file
        data        ([{}])  timing data
        
        Notes
        -----
        If pathname has no extension the string ".dat" is
        appended
        """
        
        if '.dat' not in pathname:
            pathname = pathname + ".dat"
            
        f = open(pathname, 'w')
        
        for dic in data:
            if 'mainTimer' == dic['what'] and 'cores' in dic:
                f.write("\t\t num Nodes    CPU tot   Wall tot\n")
                f.write("=" * 48 + "\n")
                f.write(dic['what'] + "\t\t" + str(dic['cores']) + "    " + \
                    str(dic['cpu tot']) + "    " + str(dic['wall tot']) + "\n")
                f.write("\n\t\t\t CPU max\t Wall max\t CPU min\t Wall min\t CPU avg\t Wall avg\n")
                f.write("=" * 115 + "\n")
            else:
                # 16. Jan. 2017
                # http://stackoverflow.com/questions/20309255/how-to-pad-a-string-to-a-fixed-length-with-spaces-in-python
                f.write("{:<20}".format(dic['what']) + "\t")
                f.write("{:<10}".format(str(dic['cpu max'])) + "\t")
                f.write("{:<10}".format(str(dic['wall max'])) + "\t")
                f.write("{:<10}".format(str(dic['cpu min'])) + "\t")
                f.write("{:<10}".format(str(dic['wall min'])) + "\t")
                f.write("{:<10}".format(str(dic['cpu avg'])) + "\t")
                f.write("{:<10}".format(str(dic['wall avg'])))
                f.write("\n")
        
        f.close()
