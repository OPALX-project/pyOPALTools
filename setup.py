from setuptools import setup, find_packages

DISTNAME = 'opal'
VERSION = '1.0.0'

# For running the jupyter notebooks, in addition the modules
# * jupyter
# * notebook
# are required
INSTALL_REQUIRES = [
    'chaospy>=3.2.9',
    'h5py>=2.9.0',
    'matplotlib>=3.0.3',
    'numpy>=1.16.2',
    'pandas>=0.24.2',
    'plotly>=3.7.0',
    'scipy>=1.2.1',
    'seaborn>=0.9.0',
    'scikit-learn',
    'yt>=3.5.1'
]

if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=VERSION,
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        zip_safe=False,
        python_requires='>=3.8',
        package_data={'opal.utilities': ['log.yaml']},
        url="https://gitlab.psi.ch/OPAL/pyOPALTools",
    )
