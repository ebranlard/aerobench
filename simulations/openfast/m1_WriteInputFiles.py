import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob    
import os
# Local 
import weio
import welib.fast.fastlib as fastlib
import welib.tools
from helper_functions import *

templateDir='templates/straight/'

cone  = np.arange(-50, 51, 5)
yaw   = np.arange(-50, 51, 5)

R, R_blade, rho, U0, RPM = getSimParams()

exe = './aerodyn_driver.exe'

# --- For prebend
f = weio.read(os.path.join(templateDir, 'AD_blade_straight.dat'))
M = f['BldAeroNodes']
r = M[:,0]
r_bar = r/R_blade
M[:,2] = 0 # No Sweep 0BlSpn        1BlCrvAC        2BlSwpAC        3BlCrvAng       4BlTwist        BlChord          BlAFID
unit_bend = 1-np.cos(r_bar*np.pi/2)

# --- PArametric studies 
for study in ['yaw']:
    dirs=[] # directories

    if study=='cone':
        generate('_'+study+'/bem', templateDir+'driver.dvr'              , exe, proj=2, var=cone, varname='PreCone(1)', dirs=dirs )
        writeBatch(dirs); dirs=[]
        generate('_'+study+'/fvw', templateDir+'driver_olaf.dvr'         , exe, proj=3, var=cone, varname='PreCone(1)', dirs=dirs )
        writeBatch(dirs, 'OLAF')

    elif study=='yaw':
        generateYaw('_'+study+'/bem', templateDir+'driver.dvr'           , exe, proj=2, var=yaw, dirs=dirs, bemmod=250)
        writeBatch(dirs); dirs=[]
        generateYaw('_'+study+'/fvw', templateDir+'driver_olaf.dvr'      , exe, proj=3, var=yaw, dirs=dirs)
        writeBatch(dirs, 'OLAF')
