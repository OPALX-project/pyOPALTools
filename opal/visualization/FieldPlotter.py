# Copyright (c) 2020, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

from .BasePlotter import *

class FieldPlotter(BasePlotter):

    def __init__(self):
        pass

    def plot_slice(self, field, normal, pos, step=0):
        ix, iy, field = self.ds.getSlice(field, normal, pos, step)
        plt.pcolormesh(ix, iy, field)
        plt.colorbar()
        return plt
