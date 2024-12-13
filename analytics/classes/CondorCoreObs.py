# This module contains the core objects for an 
# initial Condor Funds Workflow.
# There is no warranty or guarantee of any kind 

# Analytics dir path *USER SET*
analyticsDir = '/Users/rtasseff/projects/condor_test/analytics'

import sys
# adding analytics to the system path
sys.path.insert(0, analyticsDir)


import numpy as np
import datetime

from . import genStats as gs
from . import genFin as gf
from . import utils

from data_mining import load

class PriceLoader:
    def __init__(self,path, dateH='Date', priceH='Adj Close', 
        symH='Symbol', sep=','):
        # A price loader can be created with just the path for the data
        self.path = path
        self.dateH = dateH 
        self.priceH = priceH
        self.symH = symH
        self.sep = sep
        self.syms = None

    def set_target_asset_symbols(self,syms):
        # You can set the assets for repeated use if you want
        # by design we do not keep the whole data table in memory 
        # but we can keep all the info to quickly load what is needed
        self.syms = syms
    
    def get_assets_dataFrame(self,syms=None):
        # given a list of strings for asset syms return pandas data frame
        # rows as matching dates, cols as assets, values as listed under price header
        # if no syms are passed we assume the preset values, if they exist
        if syms is not None:
            self.syms = syms 

        if self.syms is None:
            raise Exception('No symbol list is set, you must provide a list of assets to lad')
        # get data
        df = load.multiAssetHist_CSV(path, dateH=self.dateH, priceH=self.priceH, 
                symH=self.symH, sep=self.sep, verb=False)

        df = df[syms]
        
        return df

    def get_assets_np(self,syms=None):
        # given a list of strings for asset syms return a set of numpy arrays
        # - price data 2D array rows as matching dates, cols as assets, values as listed under price header
        # - 1D array for dates (should be DateTime format)
        # - 1D array for symbols (should be strs)
        # if no syms are passed we assume the preset values, if they exist
        df = self.get_assets_dataFrame(syms=syms)
        
        return utils.df2np(df)

    def get_assets(self,symList=None):
        # given a list of strings for asset syms return a list of asset objects
        # rows as matching dates, cols as assets, values as listed under price header
        # if no syms are passed we assume the preset values, if they exist
        
        # get the data
        prices, dates, syms = self.get_assets_np(syms=symList)

        # setup the data loader for the assets 
        priceLoader = PriceLoader(self.path, dateH=self.dataH, priceH=self.priceH, 
                symH=self.symH, sep=self.sep)


        # start making the assets
        n = len(syms)
        assets = []
        for i in range(n):
            # modify dataloader for this single asset 
            priceLoader.set_assets([syms[i]])
            data = TimeCourse(dates,prices[:,i],name=self.priceH)
            # at some point we may want to provide an option to the 
            # user so that the name of the price header column 
            # in the data file, does not need to be the time
            # of the time series data object
            # as we may be intrested in merging asset data from different files
            # that use different string names for the same data

            # we pass the price loader (for postarity) but we override it
            # since we have all the data here why require the user to 
            # loop through and load each seperatly 
            assets.append(Asset(syms[i], priceLoader, prices=data))

        




class TimeCourse:
    def __init__(self, times, values, name='Time Course'):
        # assuming time as a numpy array of DateTime objects
        # values is a numpy array of corrisponding values
        # name is arbitrary 
        self.times = times
        self.values = values
        self.name = name
        self.update = datetime.datetime.now() # need to double check format

class Return():
    return is a special version of time course - need to inherate 
    initalize the object just with the properties
    we should me the note (below) on space vs time to the top of this files
    returns
    expectedReturn
    returnDispersion
    returnParameters - maybe this is a dictionary??
        frequency, period, method, timeframe, metric ...

class Asset:
    __init__(self, sym, dataLoader, prices=None, method='Robust'):
        # we have purposfully made this object a bit atypical 
        # interms of how attributes are set and used directly sometimes and not others
        # this is to allow future flexibility in memory space vs compute time
        # for optimization we may not want to always recalculate the return and related properties
        # but if we are storing tons of assets in memory for real-time investingating 
        # and ultimatly we only really pick apart a few properties of a few assets
        # we may not want to pre calculate all properties for all assets
        # and just hold them in memory
        #
        # symbol is the only thing required for an asset 
        # but folks may want to regularly define it more
        # completly by passing in prices from the start.
        # Prices is just a TimeCourse object for relevant prices
        # method is a string that will decide how to update stuff
        self.sym = sym
        self.method = method
        self.returnExp = None
        self.returnDisp = None
        self.returns = # set up a return object but don't calculate anything yet
        # *** check the symbol and the target asset symbol are the same

    def load_prices_from_data(self):

    def update_prices(self, prices=None):
        # reload or set prices, clear out other attributes (return stuff), set update time
        # *** if a price object use that instead of relaoding from data
        if prices is None:
            # *** load prices using data loader
            # set update time
        else:
            # assume prices are set correctly without loading
            # *** just set prices
        # celar out other attributes and update time
            




    def update_return_properties(self):
        # *** use existing price to reset attributes for other properties
        self.returnExp = 
        self.returnDisp = gf.returnDisp(self.prices.values, method=self.method)
        self.updated = datetime.datetime.now() # need to double check format

    def set_prices(self,prices):
        # override the data loader, erase all properties 
        self.prices = prices
        self.update()

    def set_return_parameters(self,method):
        # *** we will need more than just method, time scale and type of return too
        self.method = method
        self.update()

    def calc_returns():
    def calc_expected_return():
        gf.returnExp(self.prices.values, method=self.method)
    def calc_return_dispersion():




class Portfolio:
    def __init__(self, assets, weights, *args, **kwargs):
        # a portfolio is just a list of asset objects, assets,
        # and there weights, floats.
        # but folks may want to set other attributes from the start.
        self.assets = assets
        self.weights = weights


