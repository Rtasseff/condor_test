# general finance functions for Condor workflows

import numpy as np

def _return(x0,xi,metric):
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
        r.append(_return(x[i],x[i+period],metric=metric))

    return np.array(r)


def returnExp(r, method='Robust'):
    """Calculate the expected return given given a
    set of returns,r.

    :param r:   float array, precalculated returns
    :param method:  str, what method to use,
        Possibilities
            Robust (default)    robsut statistics, median of set
            Normal              assume normal dist, mean of set
    :return rExp:   float, expected value of return set
    """
    if method=='Robust':
        rExp = np.median(r)
    elif method=='Normal':
        rExp = np.mean(r)
    else:
        raise Exception('Method not known: '+method)
    return rExp

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


def flag_dev_event(time,price,priceTrend,thresh):
    """Move through the time series, (time ,price), 
    and flag the deviation events, values that the 
    price deviates from the price trend by a given 
    threshold. 

    :param t:   datetime array, n time points for time series data
    :param price:   float array, n prices for time series data
    :param priceTrend:  float array, n predicted trend values for 
                        prices in time series data
    :param thresh:  float, threshold value for flagable deviation
    
    :return eventInd:   int list, m index values corresponding to 
                        the index, i, in array t at which a deviation 
                        event occured: |price_i-priceTrend_i|>thresh
    :return eventTime:  datetime list, m time points at which a deviation
                        event occured
    :return eventLength:    timedelta('ns') list, m lenghts in nanoseconds, 
                            corresponding to each deviation event
    """
    n = len(time)
    value = np.abs(price-priceTrend)
    eventTime=[]
    eventInd=[]
    eventLength=[]
    started=False 
    for i in range(n):
        if (value[i]>=thresh) and (started==False):
            # deviation past threshold, start timer
            started=True
            # track when this event started
            startTime=time[i]
            # record
            eventTime.append(time[i])
            eventInd.append(i)

        elif started and (((value[i]<thresh) and (started==True)) or i==(n-1)):
            # deviation under threshold threshold or series end, end timer
            # note: logic writen so events only end after they started
            # note: logic writen to end open events at end of time series
            started=False
            # get length of event that just ended
            endTime=time[i]
            # record
            eventLength.append(endTime-startTime)
            

    return eventInd, eventTime, eventLength
