# Author:    Ryan Roussel
# Date:      June 2018

def writeDistribution(distribution,fname):
    """
    Writes a particle distribution to a file for use in opal FROMFILE command

    Parameters
    ----------
    distribution   (numpy.ndarray)      array of 6D particle coordinates
                                        shape = Nx6, N == number of particles
                                        coordinates, x[m],px[beta*gamma],t[s] 
                                             [x,px,y,py,z,pz] (injected)
                                             [x,px,y,py,t,pz] (emitted)
    fname          (str)                Filename 
    """

    with open(fname,'w+') as f:
        f.write('{}\n'.format(len(distribution)))
        for particle in distribution:
            f.write('{} {} {} {} {} {}\n'.format(*particle))
