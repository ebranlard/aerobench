import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob    
import os
# Local 
from welib.tools.colors import *
import welib.fast.fastlib as fastlib

from helper_functions import *

cone = np.arange(-50,51,5)
yaw = np.arange(-50,51,5)

colrs = python_colors()      
xlim=None
plotType=2
STYs = {
       'bem':{'label':'Baseline', 'lw':1.9, 'ls':':' , 'm':None, 'c':colrs[2]},
       'fvw':{'label':'OLAF'    , 'lw':1.9, 'ls':'',   'm':'^' , 'c':colrs[4]},
      }


studies={}
algos         = ['fvw','bem']
Suffix='YAWComp_'
studies['yaw']  = postpro('yaw', yaw, algos=algos)

#studies['cone'] = postpro('cone', yaw, algos=algos)

save_results(studies)

print('>>> studies',studies.keys())

# --- Load all results or only some studies
# studies = load_results(studies_names, algos=algos)
studies_names=studies.keys()

for study in studies_names:
    plot(study, studies, algos, STYs, Suffix, plotType=plotType,xlim=xlim)






plt.show()
