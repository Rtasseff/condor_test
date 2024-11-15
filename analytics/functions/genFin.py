# general finance functions for Condor workflows

import numpy as np
from . import genStats

def calc_return(x0,xi,metric):
    """Calculate return given price x at 0 and i.

    :param x0:  float, start price
    :param xi:  float, end price
    :param metric:  str, what type of return, 
        Possibilities
            Relative (default)      ( xi - x0 ) / x0
            Delta                   xi - x0 )
            Simple                  xi / x0
            Log                     log( xi / x0 )

    """

    if metric=='Simple':
        r = xi/x0
    elif metric=='Log':
        r = np.log(xi/x0)
    elif metric=='Relative':
        r = (xi-x0)/x0
    elif metric=='Delta':
        r = ( xi-x0 )

    else:
        raise Exception('Metric not known: '+metric)
    return(r)

def returns(x,period=21,metric='Relative'):
    """Calculate the returns over a set period
    given an array of asset prices, x.
    
    Assumes all entries in x are consecutive.

    :param x:   float array, consecutive prices
    :param period:  int, period for returns,period or 
        lag or number of consecutive points to consider,
        default = 21 (rough estimate of consecutive open
        market days in a month).
    :param metric:  str, what type of return, 
        Possibilities
            Relative (default)      ( x_[t=period] - x_0 ) / x_0
            Delta                   x_[t=period] - x_0 )
            Simple                  x_[t=period] / x_0
            Log                     log( x_[t=period] / x_0 )
    :return r:  float array, seris of returns using set metric  
    """
    n = len(x)
    r = []
    for i in range(0,n-period,1):
        r.append(calc_return(x[i],x[i+period],metric=metric))

    return np.array(r)


def returnExp(r, method='Robust'):
    """Calculate the expected return given a
    set of returns,r.

    :param r:   float array, precalculated returns
    :param method:  str, what method to use,
        Possibilities
            Robust (default)    robsut statistics, median of set
            Normal              assume normal dist, mean of set
    :return rExp:   float, expected value of return set
    """
    
    rExp = genStats.expected(r,method=method)

    return rExp

def returnDisp(r, method='Robust'):
    """Calculate the dispersion of returns given a
    set of returns,r.

    :param r:   float array, precalculated returns
    :param method:  str, what method to use,
        Possibilities
            Robust (default)    robsut statistics, MAD normal adjusted 
            Normal              assume normal dist, standard deviation
    :return rDisp:   float, dispersion value of return set
    """
    if method=='Robust':
        # currently assuming MAD for robust, other options exist
        method='MAD'

    rDisp = genStats.disper(r,method=method)
    return rDisp

def calc_return_prop(r,method='Robust'):
    """Calculate the key properties of a set of returns,r.
    This will be the expected value and the measure of 
    disspersion, which can be used as risk.
    
    See supporting methods for more comments:
    calls returnExp for the expected value
    calls returnDisp for the dispersion metric 

    :param r:   float array, precalculated returns
    :param method:  str, what method to use,
        Possibilities
            Robust (default)    robsut statistics - no dist assumption 
            Normal              assume normal dist
    :return rExp:   float, expected value of return set
    :return rDisp:   float, dispersion value of return set
    """
    rExp = returnExp(r,method=method)
    rDisp = returnDisp(r,method=method)
    return rExp, rDisp
 


def prices2returnExp(x,period,metric='Relative', method='Robust'):
    """Convert array of prices,x, to an array of returns.
    Assumes all entries in x are consecutive.

    :param x:   float array, consecutive prices
    :param period:  int, period for returns, period or 
        lag or number of consecutive points to consider,
        default = 21 (rough estimate of consecutive open
        market days in a month).
    :param metric:  str, what type of return, 
        Possibilities
            Relative (default)      ( x_[t=period] - x_0 ) / x_0
            Simple                  x_[t=period] / x_0
            Log                     log( x_[t=period] / x_0 )
    :param method:  str, what method to for estimating return,
        Possibilities
            Robust (default)    use robust statistics 
            Normal              assume normal dist
    :return rExp:   float, expected value of return set
    """
    r = returns(x,period=21,metric=metric)
    rExp = returnExp(r, method=method)
    return(rExp)

def dev(price,exp):
    """ Give the deviation of the actual price, price,
    from the expected price, exp, relative to the 
    expected price.
    """
    dev = (price - exp)/exp
    return dev






