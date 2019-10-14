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
