# Author:   Matthias Frey
# Date:     April 2018

from operator import itemgetter

def mostConsuming(n, times, labels, prop):
    """
    Retturn time and label of the first n most time
    consuming timings.
    
    Parameters
    ----------
    n       (int)   number of timings
    times   ([])    list of timing data
    labels  ([])    list of labels to appropriate timings
    
    Returns
    -------
    sorted times and labels
    """
    # 15. Jan. 2017,
    # http://stackoverflow.com/questions/9543211/sorting-a-list-in-python-using-the-result-from-sorting-another-list
    times_sorted, labels_sorted = zip(*sorted(zip(times, labels),
                                              key=itemgetter(0),
                                              reverse=True))
    
    return list(times_sorted[0:n]), list(labels_sorted[0:n])
