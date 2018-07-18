# Author:     Ryan Roussel
# Date:       June 2018

import numpy as np
import logging

def gaussian(nParticles,standardDeviations,pCentral,**kwargs):
    """
    Generates a 6D gaussian distribution with no directional correlations
    (diagonal covarience matrix and zero mean)

    Parameters
    ----------
    nParticles         (int)      number of particles to generate
    standardDeviations (ndarray)  (6,) standard deviation of distribution in each direction
    pCentral           (float)    central momentum in beta*gamma_z

    Optionals
    ---------
    cov                (ndarray)  (6,6) full covarience matrix
    mean               (ndarray)  (6,) mean loactions

    Returns
    -------
    data               (ndarray)  (N,6) array with 6D particle coordinates

    """
    cov = kwargs.get('cov',np.diag(np.square(standardDeviations)))
    mean = kwargs.get('mean',[0,0,0,0,0,pCentral])
    #logging.info(cov)
    #logging.info(mean)
    
    return np.random.multivariate_normal(mean,cov,nParticles)


def uniform(nParticles,size,pCentral,**kwargs):
    """
    Generates a 6D unifrom distribution with no directional correlations
    (zero mean)

    Parameters
    ----------
    nParticles         (int)      number of particles to generate
    size               (ndarray)  (6,) width of distribution in each direction
    pCentral           (float)    central momentum in beta*gamma_z

    Returns
    -------
    data               (ndarray)  (N,6) array with 6D particle coordinates

    """
    #random data for each dimention, from [-1,1]
    avg = [0,0,0,0,0,pCentral]
    data = np.random.random_sample((nParticles,6))*2.0 - 1.0
    
    #scale data to size
    scaled_data = np.asfarray([ele*scale + shift for ele,scale,shift in zip(data.T,size,avg)]).T
    
    return scaled_data
