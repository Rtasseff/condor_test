# scripts to load simple files for condor 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def assetHist_CSV(path, dateH='Date', priceH='Adj Close**',
        sep=',', disp=True, verb=True, assetN='Asset'):
    """Load a simple flat file for asset data date and price.
    :param path:    path to file
    :param dateH:   date header
    :param priceH:  price header
    :param sep: seperation char
    :param disp:    display plot if true
    :param verb:    display verbose details if true
    :param assetN:  asset name string
    :return x:  date string list
    :return y:  closing price numpy array
    """

    data = pd.read_csv(path, sep=sep)
    # Convert date column to datetime
    data[dateH] = pd.to_datetime(data[dateH])


    
    # Preference to see data start to end so flip it if needed
    data.sort_values(dateH, axis=0, ascending=True, inplace=True)

    #take a look
    data.info()
    data

    # Plot the data for sanity check
    plt.figure(figsize=(8, 6))
    plt.plot(data[dateH], data[priceH])
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price ($)')
    plt.title(assetN+' Pricing History')
    plt.show()

    return data[dateH].to_numpy(), data[priceH].to_numpy()
    





