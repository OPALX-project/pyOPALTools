from setuptools import setup, find_packages

setup(
    name="opal",
    version="1.0.0",
    packages=find_packages(),

    install_requires=[
        'h5py>=2.7.1',
        'jupyter>=1.0.0',
        'matplotlib>=2.1.0',
        'notebook>=5.2.0',
        'numpy>=1.13.3',
        'pandas>=0.21.0',
        'pickleshare>=0.7.4',
        'plotly>=2.5.1',
        'scipy>=0.19.1',
        'seaborn>=0.8.1'
    ],
    
    url="https://gitlab.psi.ch/OPAL/pyOPALTools",
)