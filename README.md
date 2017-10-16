Setup:

export PYTHONPATH=xxx/pyOPALTools:$PYTHONPATH

Then checkout the test directory

Python Package Dependencies  
===========================
h5py  
numpy  
matplotlib  
scipy
jupyter [notebook]




Installation of a virtual Python environment
===========================
It is recommended to create a virtual Python environment. You might need to install [Python3](https://www.python.org/) first.
The *pyOPALTools* environment is installed with following steps:

```bash
virtualenv -p `which python3` pyOPALTools.venv
source pyOPALTools.venv/bin/activate
```

The virtual environment can be deactivated with 

```bash
deactivate
```

Install Jupyter and additional software in the *activated* environment

```bash
pip install numpy
pip install scipy
pip install jupyter\[notebook\] matplotlib
pip install h5py
```

### Run Jupyter
A Jupyter notebook is started by executing

```bash
jupyter notebook
```