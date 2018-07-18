import numpy as np
import matplotlib.pyplot as plt
import logging

from scipy import misc
   
def plot_mask(fname,xsize,ysize,ax=''):
    mask = misc.imread('test_mask.png',flatten=True)
    mask_shape = mask.shape
    
    x = np.linspace(0,xsize,mask_shape[0])
    y = np.linspace(0,ysize,mask_shape[1])
    xx,yy = np.meshgrid(x,y)
    
    if not ax:
        fig,ax = plt.subplots()

    ax.contourf(xx,yy,mask)
    return ax

def mask_distribution(fname,dist,xsize,ysize,centered=True):
    '''
    dist (ndarray, size = Nx6, N==number of particles) 
    '''
    image_data = misc.imread(fname,flatten=True)

    #calcuate grid properties
    shape = image_data.shape
    if centered:
        x = np.linspace(-xsize/2.0,xsize/2.0,shape[0])
        y = np.linspace(-ysize/2.0,ysize/2.0,shape[1])
    else:
        x = np.linspace(0,xsize,shape[0])
        y = np.linspace(0,ysize,shape[1])


    out_dist = []

    for part in dist:
        #find x and y indicies of where particle falls on mask
        try:
            x_index = np.searchsorted(x,part[0])
            y_index = np.searchsorted(y,part[2])

            #get color value at index
            c = image_data.T[x_index][y_index]
        
            if not c:
                out_dist.append(part)
        except IndexError:
            pass

    return np.asfarray(out_dist)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    main()
    plt.show()
