# Author: Ryan Roussel
# Date:   June 2018
import numpy as np

class ElementParser:
    def __init__(self):
        self.filename = ''
        self.element_outlines = []
        self.element_centerlines = []
        self.element_entrances = []
        self.element_exits = []

    def parse(self,fname):
        self.filename = fname
        __raw_data = []
        __temp_data = []

        with open(fname) as f:
            for line in f:
                __line_data = line.strip().split('    ')
                if len(__line_data) == 2:
                    __temp_data.append(__line_data)
                else:
                    __raw_data.append(np.asfarray(__temp_data))
                    __temp_data = []
        
        for ele in __raw_data:
            if not ele.shape[0] == 2:
                self.element_outlines.append(ele)
            else:
                self.element_centerlines.append(ele)


