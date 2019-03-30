from setuptools import setup, find_packages

DISTNAME    = 'opal'
VERSION     = '1.0.0'

PACKAGES = [
    'opal',
    'opal.analysis',
    'opal.datasets',
    'opal.parser',
    'opal.timing',
    'opal.utilities',
    'opal.visualization',
    'opal.visualization.statistics',
    'opal.visualization.styles'
]

INSTALL_REQUIRES = [
    'h5py>=2.7.1',
    'jupyter>=1.0.0',
    'matplotlib>=2.1.0',
    'notebook>=5.2.0',
    'numpy>=1.13.3',
    'pandas>=0.21.0',
    'pickleshare>=0.7.4',
    'plotly>=2.5.1',
    'scipy>=0.19.1',
    'seaborn>=0.8.1',
    'pyaml>=18.11.0'
]


if __name__ == "__main__":
    setup(
        name=DISTNAME,
        version=VERSION,
        packages= PACKAGES, #find_packages(),
        #include_package_data = True,
        install_requires=INSTALL_REQUIRES,
        #dependency_links=['https://gitlab.psi.ch/OPAL/pyOPALTools/tags/test-1.0.0'],
        zip_safe=False,
        python_requires='>=3.0',
        
        url="https://gitlab.psi.ch/OPAL/pyOPALTools",
    )
