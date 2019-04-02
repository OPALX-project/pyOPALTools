##
# @author Matthias Frey
# @date 2016 - 2017
#

import pickle as pickle
import pprint
import re


class TimingParser:

    """
    Read and write an Ippl timing file.
    
    Example:
    
    import TimingParser as timing
    
    time = timing.TimingParser()
    
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
        
        self._special_dict = {'what':     [],
                              'cpu max':  [],
                              'wall max': [],
                              'cpu min':  [],
                              'wall min': [],
                              'cpu avg':  [],
                              'wall avg': []}
        return main_dict, self._special_dict
    
    
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
        
        self._problem = {}
        self._data = []
        
        main_dict, special_dict = self._init_data_structure()
        
        # 13. July 2017
        # https://stackoverflow.com/questions/2301789/read-a-file-in-reverse-order-using-python
        lines = []
        special_count = 0
        main_count = 0
        
        for line in reversed(open(f).readlines()):
            if "Timings{" in line:
                lines.insert(0, line)
        
        core_pattern = '.*> Timing results for (.*) nodes:'
        main_pattern = '.*> (.*) Wall tot = (.*), CPU tot = (.*)'
        max_pattern = '.*> (.*) Wall max = (.*), CPU max = (.*)'
        avg_pattern = '.*> Wall avg = (.*), CPU avg = (.*)'
        min_pattern = '.*> Wall min = (.*), CPU min = (.*)'
        
        # we parse it the right order
        for line in lines:
            
            line = ' '.join(line.split())
            
            obj = re.match(core_pattern, line)
            
            
            if obj:
                main_dict['cores'] = obj.group(1)
                main_count += 1
                continue
            
            obj = re.match(main_pattern, line)
            
            if obj:
                # main timer
                main_dict['what'] = obj.group(1).replace('.', '')
                main_dict['wall tot'] = float(obj.group(2))
                main_dict['cpu tot'] = float(obj.group(3))
                main_count += 1
                continue
            
            # special timings have 3 lines
            obj = re.match(max_pattern, line)
                
            if obj:
                special_dict['what'] = obj.group(1).replace('.', '')
                special_dict['wall max'] = float(obj.group(2))
                special_dict['cpu max'] = float(obj.group(3))
                special_count += 1
                continue
                
            obj = re.match(avg_pattern, line)
            
            if obj:
                special_dict['wall avg'] = float(obj.group(1))
                special_dict['cpu avg'] = float(obj.group(2))
                special_count += 1
                continue
            
            obj = re.match(min_pattern, line)
            
            if obj:
                special_dict['wall min'] = float(obj.group(1))
                special_dict['cpu min'] = float(obj.group(2))
                special_count += 1
            
            if special_count == 3:
                special_count = 0
                self._data.append(dict(special_dict))
            
            if main_count == 2:
                main_count = 0
                self._data.append(dict(main_dict))
    
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
        
        self._problem = {}
        self._data = []
        
        main_dict, special_dict = self._init_data_structure()
        
        problem_pattern = '(.*): (\d+)'
        main_pattern = '(.*) (\d+) (.*) (.*)'
        special_pattern = '(.*) (\d+) (.*) (.*) (.*) (.*) (.*) (.*)'
        
        with open(f, 'r') as ff:
            
            for line in ff:
                
                if 'num Nodes' in line:
                    tag = self._order(line, 2)
                    continue
                
                # 2. Feb. 2018
                # https://stackoverflow.com/questions/2077897/substitute-multiple-whitespace-with-single-whitespace-in-python
                line = ' '.join(line.split())
                
                obj = re.match(problem_pattern, line)
                
                if obj:
                    self._problem[obj.group(1).lstrip()] = int(obj.group(2))
                    continue
                
                obj = re.match(main_pattern, line)
                
                if obj:
                    # remove appending dots "..." of timing names
                    main_dict['what']       = obj.group(1).replace('.', '')
                    main_dict['cores']      = obj.group(tag['num nodes'])
                    main_dict['cpu tot']    = float(obj.group(tag['cpu tot']))
                    main_dict['wall tot']   = float(obj.group(tag['wall tot']))
                    # we need to copy otherwise it overwrites the data
                    self._data.append(dict(main_dict))
                    # clear pattern otherwise special timings go in here too
                    main_pattern = '-1'
                    continue
                
                obj = re.match(special_pattern, line)
                
                if obj:
                    special_dict['what']        = obj.group(1).replace('.', '')
                    special_dict['cpu max']     = float(obj.group(tag['cpu max']).strip())
                    special_dict['wall max']    = float(obj.group(tag['wall max']).strip())
                    special_dict['cpu min']     = float(obj.group(tag['cpu min']).strip())
                    special_dict['wall min']    = float(obj.group(tag['wall min']).strip())
                    special_dict['cpu avg']     = float(obj.group(tag['cpu avg']).strip())
                    special_dict['wall avg']    = float(obj.group(tag['wall avg']).strip())
                    # we need to copy otherwise it overwrites the data
                    self._data.append(dict(special_dict))
                    continue
    
    
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
    
    @property
    def properties(self):
        return self._special_dict
    
    
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
