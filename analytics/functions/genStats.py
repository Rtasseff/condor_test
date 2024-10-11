# general statistics functions for Condor workflows


import matplotlib.pyplot as plt
import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa import stattools


def run_model(X,y):
    # statsmodels ordinary least squares regression model
    regr = OLS(y, X, missing='drop').fit()
    ic = regr.bic
    rsq = regr.rsquared_adj
    yHat = regr.predict(X)
    
    return ic, rsq, yHat, regr

def x2X(x,modelName):

    # parse the model name 
    words = modelName.split(" ")

    if words[0] == 'Polynomial':
        polyOrder = int(words[2])
        for order in range(polyOrder):
            # Create X matrix
            if order == 1:
                X = add_constant(x.reshape(-1, 1))
            else:
                X = np.c_[X, x**order]


    elif words[0] == 'Exp Function':
        X = add_constant(x.reshape(-1, 1))

    elif words[0] == 'Log Function':
        X = add_constant(np.log(x+1).reshape(-1, 1))

    else:
        raise Exception('Model name not known: '+modelName)
    return X



def fit_simp_model(x,y,maxPolyOrder):
    """Given an array, x, of independant variables and 
    a corrisponding array, y, of dependant variables,
    we cycle through several simple models to select the best
    based on adjusted r-squared value.
    The models include polynomial fits up to order maxPolyOrder,
    an exponental function and a logrithmic function.
    This is for a single feature, variable system (e.g. time course).

    Note: that currently the BIC is not comparable between the exp
    model and the others because there is a transformation in y
    prior to the model fit.
    Since the BIC is calculated during the fit the residuals are off 
    by orders of magnatude.
    This is why we are using adjusted r-squared
    :param x:   float array, independant variable, feature
    :param y:   float array, dependant variable, observables, regressors
    :param maxPolyOrder:    int, the maximum order polynomial to be considered (Note: 7 or more usually has errors)
    :return rsqAdjBest: float, adjusted r squared for the best model id'ed
    :return nameBest:   str, name of the best model id'ed  
    :return modelBest:  object, statsmodels OLS model object of the best model id'ed
    :return yHatBest:   float array, returned y values evaluated on the best model id'ed 
    """

    nameBest = ''
    modelBest = ''
    yHatBest = []
    rsqAdjBest = 0 
    # we decided to use adjusted r squared here because the ics
    # calculated in stats ols function are not comparable if a
    # variable transformation is done on y prior to the function
    # call, which is what we do in exp.
    # However, this should not be an issue given the small number 
    # of parameters for these models.
    if len(y) < maxPolyOrder*4: 
        print('Warning: Low obs to order, double check model selection criterion')

    # Run through all poly deg models
    for i in range(maxPolyOrder):
        polyOrder = i+1
        name = 'Polynomial Order '+str(polyOrder)

        # Create X matrix
        X = x2X(x,name)
        
        ic, rsqAdj, yHat, model = run_model(X,y)
        
        if rsqAdj > rsqAdjBest:
            rsqAdjBest = rsqAdj
            nameBest = name
            modelBest = model
            yHatBest = yHat
        
    


    ### Run for exp function: y=Aexp(Bx) -> log(y)=log(A)+Bx
    name = 'Exp Function'

    X = x2X(x,name)
    ic, rsqAdj, yHatLog, model = runModel(X,np.log(y))
    
    if rsqAdj > rsqAdjBest:
        rsqAdjBest = rsqAdj
        nameBest = name
        modelBest = model
        yHatBest = np.exp(yHatLog)


    ### Run for log function: y=A+Blog(x)
    name = 'Log Function'

    X = x2X(x,name)
    ic, rsqAdj, yHat, model = run_model(X,y)

    if rsqAdj > rsqAdjBest:
        rsqAdjBest = rsqAdj
        nameBest = name
        modelBest = model
        yHatBest = yHat


    return rsqAdjBest, nameBest, modelBest, yHatBest

def acf(x,fracLag = 0.33,ci=95):
    """Calcualte the auto corelation function af an 
    *evenly spaced* sequance of data, x,
    with a confidence interval, ci percent.

    :param x:   float array, consecutive and evenly spaced (in time) data points
    :param fracLag: float, maximum lag determined by fraction full time course
    :param ci:  float, percent confidence bounds to report

    :return acf:    float array, auto correlation function values
    :return lags:   float array, lags corresponding to acf (currently 0, 1, ..., int(n*fracLag))
    :return acfConf:    float array, acf upper ([:,0]) and lower ([:,1]) acf ci values corresponding to returned acf array
    """

    # maximum lag considered is % of total 
    n = len(x)
    maxLag = int(fracLag*n)

    # For now just use a built-in, well accepted method
    acf, acfConf = stattools.acf(x,alpha=(1-ci/100),nlags=maxLag,missing='conservative')

    # final lags are just consecutive time points
    lags = np.arange(len(acf))

    return acf, lags, acfConf
