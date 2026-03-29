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

def load_style(use='default'):
    from opal.visualization.styles._compat import install_rcparams_compat
    from opal.visualization.styles.default import default
    from opal.visualization.styles.jupyter import jupyter
    from opal.visualization.styles.poster import poster

    styles = {
        'default': default,
        'jupyter': jupyter,
        'poster': poster,
    }

    if use in styles:
        from opal.utilities.logger import opal_logger

        install_rcparams_compat()
        opal_logger.info("Loading '" + use + "' plotting style")
        styles[use]()
