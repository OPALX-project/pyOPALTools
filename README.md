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
pip install pyQt5
```

### Run Jupyter
A Jupyter notebook is started by executing

```bash
jupyter notebook
```



Installation of yt
==================
Yt (http://yt-project.org/) is mainly developed for astrophysics simulations, thus, plots have all units in
kpc or Mpc, etc.\ A repository that is a fork of yt and additional OPAL classes can be downloaded by

git clone https://github.com/matt-frey/yt.git