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

import numpy as np
from opal.analysis.cyclotron import detect_peaks

class TrackOrbitAnalysis:

    def calcTurnSeparation(self, nsteps=-1, angle=0.0):
        """Calculate turn separation from OPAL xxx--trackOrbit.dat file

        Parameters
        ----------
        nsteps : int
            Number of steps per turn
        angle : float
            Angle of reference line in radians

        Returns
        -------
        float
            Turn separation
        float
            Energy
        float
            Radial angle phi_r
        float
            Radius

        Examples
        --------
        Check Cyclotron.ipynb in the opal/test directory

        """
        # first particles only
        id0s = [index for index,ID in enumerate(self.ds.getData('ID')) if ID==0]

        x  = self.ds.getData('x') [id0s]
        y  = self.ds.getData('y') [id0s]
        px = self.ds.getData('px')[id0s]
        py = self.ds.getData('py')[id0s]
        pz = self.ds.getData('pz')[id0s]

        refline = x * np.cos(angle) + y * np.sin(angle)
        # Get axis crossings
        pksx = detect_peaks(refline, mph=0.04, mpd=100)
        # Correct as peaks might not correspond to each other
        # Use number of steps per turn
        if not nsteps==-1:
            for pknr in range(1,len(pksx)):
                pksx[pknr] = pksx[pknr-1] + nsteps
                if pksx[pknr] + nsteps >= len(x):
                    break

        mx = refline[pksx]

        # Turn separation is the difference between crossings
        ts = np.diff(mx)

        # Particle energy
        p_mass = 938.28 # proton mass in MeV / c^2
        # Beta*gamma
        beta_gamma = np.sqrt(px * px + py * py + pz * pz)
        # Gamma
        gamma = np.sqrt(1+beta_gamma*beta_gamma)
        # Energy
        energy = (gamma - 1) * p_mass
        # Radius
        radius = np.sqrt( x * x + y * y)
        # Radial direction v_r (normalise with momentum?)
        phi_r = np.arctan( px / py ) - np.arctan( y / x )

        # Mask
        energy = energy[pksx]
        radius = radius[pksx]
        phi_r  = phi_r[pksx]

        return ts, energy, phi_r, radius
