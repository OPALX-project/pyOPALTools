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

import logging
import logging.config

has_yaml = True
try:
    import yaml
except:
    has_yaml = False

import os


def find_config_file():
    test = ''
    try:
        # 22. March 2019
        # https://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python
        paths = os.environ['PYTHONPATH'].split(os.pathsep)
        if paths:
            for path in paths:
                test = os.path.join(path, 'opal', 'utilities', 'log.yaml')
                if os.path.exists(test):
                    return test, True
    except:
        pass
    return test, False


path, found = find_config_file()

if found and has_yaml:
    # 22. March 2019
    # https://realpython.com/python-logging/
    with open(path, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
else:
    opal_logger = logging.getLogger('opal')
    opal_logger.setLevel(logging.ERROR)
    # 29. March 2019
    # https://docs.python.org/3/howto/logging-cookbook.html
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    opal_logger.addHandler(ch)

    

opal_logger = logging.getLogger('opal')
