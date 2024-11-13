# general statistics functions for Condor workflows


import matplotlib.pyplot as plt
import numpy as np
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from statsmodels.tsa import stattools
from scipy import stats


def fit_model(X,y):
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
        for order in range(1,polyOrder+1):
            # Create X matrix
            if order == 1:
                X = add_constant(x.reshape(-1, 1))
            else:
                X = np.c_[X, x**order]


    elif words[0] == 'Exp':
        X = add_constant(x.reshape(-1, 1))

    elif words[0] == 'Log':
        X = add_constant(np.log(x+1).reshape(-1, 1))

    else:
        raise Exception('Model name not known: '+modelName)
    return X


def run_model(x,model,modelName):
    """Run the OLS model, model, of type modelName on
    the dependant variable, x, and return the predicted 
    or dependant values, y. Note that the independant
    variable will be transformed into a design matrix
    internall based on the modelName.

    :param x:   float array, 1D array for independant varriable
    :param model:   object, results from running statsmodels's
                    OLS.fit() method
    :param modelName:   str, name of model, model type, internal 
                        convention

    return y:   float array, 1D array for predictions of model, 
                dependnat variable
    """
    y = model.predict(model.params,x2X(x,modelName))

    return y

def fit_simp_model(x, y, maxPolyOrder):
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
        
        ic, rsqAdj, yHat, model = fit_model(X,y)
        
        if rsqAdj > rsqAdjBest:
            rsqAdjBest = rsqAdj
            nameBest = name
            modelBest = model
            yHatBest = yHat
        
    


    ### Run for exp function: y=Aexp(Bx) -> log(y)=log(A)+Bx
    name = 'Exp Function'

    X = x2X(x,name)
    ic, rsqAdj, yHatLog, model = fit_model(X,np.log(y))
    
    if rsqAdj > rsqAdjBest:
        rsqAdjBest = rsqAdj
        nameBest = name
        modelBest = model
        yHatBest = np.exp(yHatLog)


    ### Run for log function: y=A+Blog(x)
    name = 'Log Function'

    X = x2X(x,name)
    ic, rsqAdj, yHat, model = fit_model(X,y)

    if rsqAdj > rsqAdjBest:
        rsqAdjBest = rsqAdj
        nameBest = name
        modelBest = model
        yHatBest = yHat


    return rsqAdjBest, nameBest, modelBest, yHatBest

def acf(x,fracLag = 0.33,ci=95):
    """Calcualte the auto corelation function of an 
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



def find_samp_freq(x, cutoff=0.05, period=21,ci=95, fracLag = 0.1):
    """Finds the appropriate sampiling period for an 
    *evenly spaced* sequance of data, x, by using the
    autocorrelation function, genStats.acf, and the 
    +/- cuttoff for 'near' zero to be maintained over 
    the given period.

    :param x:   float array, consecutive and evenly spaced (in time) data points
    :param cutoff:  float, acf value considered statistically 'near' zero, default 0.05
    :param period:  int, number of conseutive data points covering the period to maintain the cutoff
    :param ci:  float, percentage for acf confidence interval, the estimated acf ci must contain the zero for the proceedig period of the sampiling frequency

    :return sampFreq:   int, sampiling frequency, consecutive points to skip in the data sequence for a sufficently uncorrelated observations
    """
    
    # get the acf using above function def
    ac, lag, acConf = acf(x,fracLag=fracLag,ci=ci)
    
    # prep bounds for searching for the sampFreq
    sampFreq = 100000
    n = len(lag)
    
    # start sampFreq search
    for i in range(n-period):
        uncorr = True
        
        # check over the whole period from this point
        for j in range(period):

            # check if the mean is in bounds
            if np.abs(ac[i+j]) > cutoff: 
                uncorr = False
                break
                # check if the CI bounds contain zero
                if acConf[i+j,0] * acConf[i+j,1] > 0:

                    # no go, get out
                    uncorr = False
                    break
        if uncorr:
            sampFreq = lag[i]
            break

    return sampFreq


def disper(x,method='MAD'):
    """Calculate the statistical dispersion of 
    the data set, x.

    :param x:   float array, data set
    :param method:  str, method used to calculate
        Possibilities
            MAD (default)   Median Absolute Deviation with 
                            correction factor for normality
            Percentile      Determines ordered rank of the 
                            abs deviation and returns the upper
                            percentile threshold (32th highest 
                            value) 
            Normal          Assumes normal distribution and 
                            returns the standard deviation

    :return sigma:  float, spread of data compared to data centroid

    Note: they way these are defined is for a symetric dispersion
    above and below the centroid or expected value.

    Note: Nan values are removed prior to calculation
    """

    # remove nans
    x = x[~np.isnan(x)]

    if method=='MAD':
        sigma = stats.median_abs_deviation(x,scale='normal')
    elif method=='Quant':
        abDev = np.sort(np.abs(x-np.median(x)))
        sigma = abDev[int(len(x)*.68)] 
    elif method=='Normal':
        sigma = np.std(x)
    else:
        raise Exception('Model name not known: '+modelName)

    return sigma

def expected(x, method='Robust'):
    """Calculate the expected value given a
    set of values,x.

    :param x:   float array, values
    :param method:  str, what method to use,
        Possibilities
            Robust (default)    robsut statistics, median of set
            Normal              assume normal dist, mean of set
    :return xExp:   float, expected value of return set

    Note: nan values are removed
    """
    # remove nans
    x = x[~np.isnan(x)]

    if method=='Robust':
        xExp = np.median(x)
    elif method=='Normal':
        xExp = np.mean(x)
    else:
        raise Exception('Method not known: '+method)
    return xExp


    
        
