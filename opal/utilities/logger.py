import logging
import logging.config
import yaml
import os


def find_config_file():
    # 22. March 2019
    # https://stackoverflow.com/questions/1489599/how-do-i-find-out-my-python-path-using-python
    paths = os.environ['PYTHONPATH'].split(os.pathsep)
    
    test = ''
    for path in paths:
        test = os.path.join(path, 'opal', 'utilities', 'log.yaml')
        if os.path.isfile(test):
            break
    return test

# 22. March 2019
# https://realpython.com/python-logging/
with open(find_config_file(), 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

opal_logger = logging.getLogger('opal')
