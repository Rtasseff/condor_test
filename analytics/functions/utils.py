# assorted utilities for condor funds



import numpy as np



def ns2days(ns):
    """Convert an array, ns, of numpy.timedelta64 
    objects in nanoseconds to an numpy array of 
    floats in days.

    :param ns:  timedelta64 array, series of nanoseconds
    
    :return days:   float array, same series converted to days
    """
    # check to see if it is nano seconds

    if ns[0].dtype != np.dtype('<m8[ns]'):
        raise Exception('Passed object is not an numpy timedelta array in nanoseconds')

    # how many nanoseconds in a day?
    nsInDay = 86400000000000


    n = len(ns)
    days = np.ones(n)

    # no need to be fancy, just run through and convert
    for i in range(n):
        days[i] = float(ns[i])/nsInDay
    
    return days


