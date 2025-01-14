# This module contains the core objects for important curves in analysis 
# for the initial Condor Funds Workflow.
# There is no warranty or guarantee of any kind 

# Analytics dir path *USER SET*
# in the future may want to change this to assume it is the above dir 
# regardless of path

analyticsDir = '/Users/rtasseff/projects/condor_test/analytics'

import sys
# adding analytics to the system path
sys.path.insert(0, analyticsDir)

from functions import genStats as gs
from functions import genFin as gf
from functions import utils
from functions import portOpt as po

from data_mining import load




import numpy as np
import datetime

# a small number that could be considered zero compared to 1.0
eps = 1e-7


