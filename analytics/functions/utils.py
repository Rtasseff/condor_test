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

def asset_list2df(assets):
    """Take a list of Asset objects, assets, and create a price DataFrame.  
    A 2D pandas df for the data with rows as dates and cols as the price values
    """
    symH = 'Symbol'
    dateH = 'Date'
    asset = assets[0]
    priceH = asset.prices.name
    sym = asset.sym
    prices =  asset.prices.values
    dates = asset.prices.times
    n = len(prices)
    if n != len(dates):
        raise Exception('Asset '+sym+' has a different number of times and values')
    tmp = np.stack(([sym]*n,dates,prices),axis=1)
    df = pd.DataFrame(data=tmp,columns=[symH,dateH,prcieH])

    for i in range(1,len(assets),1):
        asset = assets[i]
        if priceH != asset.prices.name:
            raise Exception('Cannot join asset values with different time course names')
        sym = asset.sym
        prices =  asset.prices.values
        dates = asset.prices.times
        n = len(prices)
        if n != len(dates):
            raise Exception('Asset '+sym+' has a different number of times and values')

        tmp = np.stack(([sym]*n,dates,prices),axis=1)
        df = df.append(tmp)

    # rearrange table as dates vs symbols
    data = data.pivot_table(index=dateH, columns=symH, values=priceH)


    return df







def df2np(df):
    """Convert a dataframe into a numpy data matrix, 
    a numpy array for index and column headers.
    in the condor workflow we have been using simple numpy arrays 
    and not much on panads after the data is orginized .
    To facilitate this it is easier for us to just pull out the parts.
    We typically expect the index to be the dates and the collumns to 
    be the asset symbols.
    """
    return df.to_numpy(), df.index.to_numpy(), df.columns.to_numpy()



