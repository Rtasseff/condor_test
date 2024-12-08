# This module contains the core objects for an 
# initial Condor Funds Workflow.
# There is no warranty or guarantee of any kind 
import numpy as np
import datetime
from path here import genFin as gf

class TimeCourse:
    def __init__(self, times, values, name='Time Course'):
        # assuming time as a numpy array of DateTime objects
        # values is a numpy array of corrisponding values
        # name is arbitrary 
        self.times = times
        self.values = values
        self.name = name
        self.update = datetime.datetime.now() # need to double check format

class Asset:
    __init__(self, sym, prices=None, method='Robust'):
        # symbol is the only thing required for an asset 
        # but folks may want to regularly define it more
        # completly by passing in prices from the start.
        # Prices is just a TimeCourse object for relevant prices
        # method is a string that will decide how to update stuff
        self.sym = sym
        self.prices = prices
        self.method = method
        if prices is not None:
            # since we have prices we can set other attributes
            self.returnExp = gf.returnExp(prices.values, method=method)
            self.returnDisp = gf.returnDisp(prices.values, method=method)
            self.update = datetime.datetime.now() # need to double check format


        def update(self):
            self.returnExp = gf.returnExp(self.prices.values, method=self.method)
            self.returnDisp = gf.returnDisp(self.prices.values, method=self.method)
            self.update = datetime.datetime.now() # need to double check format

        def set_prices(self,prices):
            self.prices = prices
            self.update()

        def set_method(self,method):
            self.method = method
            self.update()



            


class Portfolio:
    def __init__(self, assets, weights, *args, **kwargs):
        # a portfolio is just a list of asset objects, assets,
        # and there weights, floats.
        # but folks may want to set other attributes from the start.
        self.assets = assets

