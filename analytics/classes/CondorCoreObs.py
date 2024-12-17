# This module contains the core objects for an 
# initial Condor Funds Workflow.
# There is no warranty or guarantee of any kind 

# Analytics dir path *USER SET*
# in the future may want to change this to assume it is the above dir 
# regardless of path
analyticsDir = '/Users/rtasseff/projects/condor_test/analytics'

from functions import genStats as gs
from functions import genFin as gf
from functions import utils

from data_mining import load


import sys
# adding analytics to the system path
sys.path.insert(0, analyticsDir)


import numpy as np
import datetime

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
            self.set_target_asset_symbols(syms=syms) 

        if self.syms is None:
            raise Exception('No symbol list is set, you must provide a list of assets to load')
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
            # in the data file, does not need to be the same 
            # as the time series data object name
            # as we may be intrested in merging asset data from different files
            # that use different string names for the same data

            # we pass the price loader (for postarity) but we override it
            # since we have all the data here. 
            # why require the user to loop through and load each seperatly 
            assets.append(Asset(syms[i], priceLoader, prices=data))

        




class TimeCourse:
    def __init__(self, times, values, name='Time Course'):
        # assuming time as a numpy array of DateTime objects
        # values is a numpy array of corrisponding values
        # name is arbitrary 
        self.times = times
        self.values = values
        self.name = name
        self.lastUpdated = datetime.datetime.now() # need to double check format

#class Return():
#    return is a special version of time course - need to inherate 
#    initalize the object just with the properties
#    we should me the note (below) on space vs time to the top of this files
#    returns
#    expectedReturn
#    returnDispersion
#    returnParameters - maybe this is a dictionary??
#        frequency, period, method, timeframe, metric ...

class Asset:
    def __init__(self, sym, priceLoader, prices=None):
        # we have purposfully made this object a bit atypical 
        # in terms of how attributes are set and used directly sometimes and not others
        # this is to allow future flexibility in memory space vs compute time
        # for example, in optimization we may not want to 
        # always recalculate the return and related properties
        # but if we are storing tons of assets in memory for real-time investingating 
        # and ultimatly we only really pick apart a few properties of a few assets
        # we may not want to pre calculate all properties for all assets
        # and just hold them in memory
        #
        # the symbol and data loader are the only things required for an asset 
        # but folks may want to regularly define it more
        # completly by passing in prices from the start.
        # Prices is just a TimeCourse object for relevant prices
        self.sym = sym
        self.priceLoader = priceLoader
        self.prices=prices

        if self.priceLoader.syms[0] != sym:
            self.priceLoader.syms = [sym]
            raise Warning('Passed PriceLoader has a different symbol definintion than the symbol you passed. PriceLoader, '+  priceLoader.syms[0] +', was overriden with '+sym)



        # at this time we do not want to precalculate any returns
        # this will force us to deal with calculation options 
        # in a direct and explicit way later to avoid confusion on how it is calculated
        # at the same time we do not want the user to be forced to make these 
        # decisions if they dont need the return info for this asset
        self.returns = None


    def update_prices(self, prices=None):
        # reload or set prices depnding on what is passed, 
        # clear out other attributes (return stuff), 
        # set update time

        if prices is None:
            # no price, then load data
            # a bit akward but if everything was defined correctly in its setup,
            # we just need (maybe later we can add some checks to loader):
            prices = self.priceLoader.get_assets()[0].prices
        
        # maybe later we can add some checks here on the prices, 
        # which by now were passed by the user or set above by the loader
        self.prices = prices

        # celar out other attributes and update time
        # wait! time was already updated when the TimeCourse object is created

        # incase returns was calculated on a prvious price data we need to reset
        self.returns = None

        # we could recalculate, but... 
        # the user may not need the returns, why make them deside on return options
        # and take up memory space and compute time to get them now

    def get_prices_lastUpdated(self):
        # get the time stamp for when the prices were last updated
        if self.prices is None:
            stamp = None
            raise Warning('Prices have never been set')
        else:
            stamp = self.prices.lastUpdated

        return(stamp)


#    def calc_returns(self, *args , **kwargs):
#        # a little open for mess, but we are pushing off all the logic
#        # and choices to a returns object
#        self.returns = Returns.__init__(*args, **args)

            






#class Portfolio:
#    def __init__(self, assets, weights, *args, **kwargs):
#        # a portfolio is just a list of asset objects, assets,
#        # and there weights, floats.
#        # but folks may want to set other attributes from the start.
#        self.assets = assets
#        self.weights = weights
#

