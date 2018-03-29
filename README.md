Setup
=====
```bash
$ export PYTHONPATH=xxx/pyOPALTools:$PYTHONPATH
```

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

#### Installation using virtualenv
If you do not have ```virtualenv``` installed, type
```bash
pip install virtualenv
```
in your terminal.
The *pyOPALTools* environment is installed with following steps:

```bash
virtualenv -p `which python3` pyOPALTools.venv
source pyOPALTools.venv/bin/activate
```
The virtual environment can be deactivated with 

```bash
deactivate
```

#### Installation using venv
```bash
python3 -m venv pyOPALTools.venv
source pyOPALTools.venv/bin/activate
```
The virtual environment can be deactivated with 

```bash
deactivate
```

### Installation of dependent packages

Install Jupyter and additional software in the *activated* environment

```bash
pip install numpy
pip install scipy
pip install jupyter\[notebook\] matplotlib
pip install h5py
pip install pyQt5
```

#### Installation using conda
```bash
conda create -p $TARGET/pyOPALTools.venv python=x.x.x
source activate $TARGET/pyOPALTools.venv
```
where ```$TARGET``` is some specified directory and ```x.x.x```
is some python version.
The virtual environment can be deactivated with 

```bash
source deactivate $TARGET/pyOPALTools.venv
```

The packages can be installed with
```bash
conda install -n pyOPALTools.venv numpy
conda install -n pyOPALTools.venv scipy
conda install -n pyOPALTools.venv jupyter
conda install -n pyOPALTools.venv matplotlib
conda install -n pyOPALTools.venv h5py
```

### Run Jupyter
#### Locally
A Jupyter notebook is started by executing

```bash
jupyter notebook
```
#### Remotely
In order to run Jupyter on a remote server but
having the web browser open on the local computer
do the following steps:
* Create an SSH tunnel:
 
```bash
$ ssh -L ssh -L hport:localhost:rport username@remote
```
 where ```hport``` is the host port, e.g. 8000 and
 ```rport``` the remote port, e.g. 8888. You have to
 replace *username* and *remote* properly.
* Start jupyter on the server (same terminal as before):

```bash
$ jupyter notebook --no-browser
```
It will write an URL to the screen that you need to
copy and paste to a browser
```bash
Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://localhost:rport/?token=...
```
The ```rport``` will be the number you specified in th SSH tunnel.
In order to run the browser on the local host you need to replace ```rport```
with the ```hport``` number.


Installation of yt
==================
Yt (http://yt-project.org/) is mainly developed for astrophysics simulations, thus, plots have all units in
kpc or Mpc, etc. A repository that is a fork of yt with additional OPAL classes can be downloaded by

```bash
git clone https://github.com/matt-frey/yt.git
```
In order to install do the following steps.

**Remark:** A full Python environment will be installed.
```bash
$ cd yt
$ mkdir build
$ cd doc
$ export DEST_DIR=/absolut/path/to/yt/build
$ bash install_script.sh
```
Then follow the instructions of yt. The following setting is tested to be fine:
```bash
INST_YT_SOURCE=1   # Should yt itself be installed from source?

# What follows are some other options that you may or may not need to change.

# If you've got a clone of the yt repository some other place, set this to
# point to it. The script will already check the current directory and the one
# above it in the tree.
YT_DIR=""

# These options can be set to customize the installation.

INST_PY3=1      # Install Python 3 instead of Python 2. If this is turned on,
                # all Python packages (including yt) will be installed
                # in Python 3.
INST_GIT=0      # Install git or not?  If git is not already installed, yt
                # cannot be installed from source.
INST_EMBREE=0   # Install dependencies needed for Embree-accelerated ray tracing
INST_PYX=0      # Install PyX?  Sometimes PyX can be problematic without a
                # working TeX installation.
INST_ROCKSTAR=0 # Install the Rockstar halo finder?
INST_SCIPY=0    # Install scipy?
INST_H5PY=1     # Install h5py?
INST_ASTROPY=0  # Install astropy?
INST_NOSE=1     # Install nose?
INST_NETCDF4=1  # Install netcdf4 and its python bindings?
INST_HG=0       # Install Mercurial or not?
```
It works with Python 2, i.e. ```INST_PY3=0```, as well, of course. Do not forget
to export the path variable, i.e.
```bash
$ export PATH=/absolute/path/to/build/bin:$PATH
```


