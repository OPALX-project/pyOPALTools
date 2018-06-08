# Author:    Ryan Roussel
# Date:      June 2018

import os
from opal.parser.ElementParser import ElementParser
from opal.datasets.DatasetBase import *

class ElementDataset(DatasetBase):
    def __init__(self,directory,fname):
        
        super(ElementDataset,self).__init__(directory,fname)
        self.__parser = ElementParser()

        self.__parser.parse('{}/{}'.format(directory,fname))
        
    def getOutlines(self):
        return self.__parser.element_outlines

    def getCenterlines(self):
        return self.__parser.element_centerlines
