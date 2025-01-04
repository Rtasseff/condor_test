# *** I think this is trash ***
#def calc_eiffcient_frontier(meanReturns, covMatrix, riskFreeRate=.03, constraintSet=(0, 1), annualize=True):
#    maxSR_Portfolio = maxSR(meanReturns, covMatrix, riskFreeRate, constraintSet, annualize)
#    maxSR_returns, maxSR_std = portfolioPerformance(maxSR_Portfolio['x'], meanReturns, covMatrix, annualize)
#    maxSR_allocation = pd.DataFrame(maxSR_Portfolio['x'], index=meanReturns.index, columns=["allocation"])
#    maxSR_allocation.allocation = [round(i * 100, 0) for i in maxSR_allocation.allocation]
#
#    minVol_Portfolio = minimizeVariance(meanReturns, covMatrix, constraintSet, annualize)
#    minVol_returns, minVol_std = portfolioPerformance(minVol_Portfolio['x'], meanReturns, covMatrix, annualize)
#    minVol_allocation = pd.DataFrame(minVol_Portfolio['x'], index=meanReturns.index, columns=["allocation"])
#
#    efficientList = []
#    targetReturns = np.linspace(minVol_returns, maxSR_returns, 100)
#    efficientAllocations = []
#    for target in targetReturns:
#        opt_result = efficientOpt(meanReturns, covMatrix, target, constraintSet, annualize)
#        efficientList.append(opt_result['fun'])
#        efficientAllocations.append(opt_result['x'])
#
#    return maxSR_returns, maxSR_std, maxSR_allocation, minVol_returns, minVol_std, minVol_allocation, efficientList, targetReturns, efficientAllocations


class EF:
    def __init__(self, assets, returnRange=None, riskFreeRate=0, annualizeBy='None'):
        # this is the Efficent Frontier given a set of assets


        returnTargets = np.linspace(returnRange[0], returnRange[1], 101)
        



#class CAL:
#    def __init__(self,

#class Ploter
