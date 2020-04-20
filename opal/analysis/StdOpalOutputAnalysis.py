# Copyright (c) 2019, Matthias Frey, Paul Scherrer Institut, Villigen PSI, Switzerland
# All rights reserved
#
# Implemented as part of the PhD thesis
# "Precise Simulations of Multibunches in High Intensity Cyclotrons"
#
# This file is part of pyOPALTools.
#
# pyOPALTools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You should have received a copy of the GNU General Public License
# along with pyOPALTools. If not, see <https://www.gnu.org/licenses/>.

class StdOpalOutputAnalysis:

    def calcRFphases(self, RFcavity):
        """Calculate the phases of individual cavities in the simulation

        Parameters
        ----------
        RFcavity : str
            Name of the RFcavity as specifed in the input file

        Returns
        -------
        list
            Phases

        Examples
        --------
        Check Cyclotron.ipynb in the opal/test directory
        """
        import re

        out_phases = []

        for i, cname in enumerate(RFcavity):
            turnNumber = 1
            file = open(self.ds.filename, "r")
            turns  = []
            phases = []
            for line in file:
                if re.search("Finished turn", line):
                    turnNumber += 1
                if re.search(cname, line):
                    phase = float(line.split()[5])
                    turns.append(turnNumber)
                    phases.append(phase)
            out_phases.append([turns,phases])
            file.close()

        return out_phases
