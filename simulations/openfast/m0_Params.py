import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy.interpolate import interp1d
from scipy.integrate import  solve_ivp #odeint
# Local 
from welib.fast.olaf import *
from welib.dyninflow.DynamicInflow import tau1_oye
import weio


# --- 
a_bar = 0.32
dt = 0.01

r_hub   = 3.970000
R_blade = 117.0290154583781
R       = r_hub + R_blade
rho     = 1.225
U0      = 9.0273
RPM     = 6.4135 

# OLAFParams(RPM, U0, R, a=a_bar, aScale=1.5,
#           deltaPsiDeg=6, nPerRot=None,
#           targetWakeLengthD=6,
#           nNWrot=8, nFWrot=2, nFWrotFree=1,
#           verbose=True, dt_glue_code=dt)

OLAFParams(RPM, U0, R, a=a_bar, aScale=1.2,
          deltaPsiDeg=6, nPerRot=None,
          targetFreeWakeLengthD=1,
          targetWakeLengthD=4.,
          nNWrot=8, nFWrot=0, nFWrotFree=0,
          verbose=True, dt_glue_code=dt)

# 
# 


if __name__ == '__main__':
    pass
