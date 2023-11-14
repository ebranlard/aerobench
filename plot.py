import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

simDir = 'simulations/'

cases=[]
cases+=['yaw']

tools = [d for d in os.listdir(simDir) if os.path.isdir(os.path.join(simDir,d))]
print('Tools:', tools)


# --- Load results
# TODO: all this will be placed in library code
colRotorAvg = ['Yaw_[deg]', 'Thrust_[N]' , 'Power_[W]']

def readRotorAvg(filename):
    try:
        df = pd.read_csv(filename, header=0)
    except:
        raise Exception('Failed to read: {filename}')
    # --- Perform QC
    for c in colRotorAvg:
        if c not in df.columns:
            raise Exception(f'Column {c} missing in file: {filename}')
    return df

def getStyle(case, tool, model):
    # TODO adapt
    iTool = sum(ord(c) for c in tool)
    if 'bem' in model:
        iSty=0
    elif 'fvw' in model:
        iSty=1
    else:
        iSty  = sum(ord(c) for c in model)
    clrs = plt.rcParams['axes.prop_cycle'].by_key()['color']
    stys = ['-', '--', '-.', ':']
    mrks = ['', 'o', 's', '^', 'D', 'v', '<', '>']
    sty_dict = {
            'c':         clrs[np.mod(iTool, len(clrs))],
            'ls':        stys[np.mod(iSty , len(stys))],
            'marker':    mrks[np.mod(iSty , len(mrks))]
            }
    return sty_dict

resCases = {}
for case in cases:
    resTools = {}
    for tool in tools:
        # Look for results and models
        pattern = os.path.join(simDir, tool, '_results', case+'_*_rotor-avg.csv')
        results = glob.glob(pattern)
        if len(results)==0:
            print(f'[FAIL] {tool} {case}: No results files found with pattern {pattern}')
            continue
        try:
            models = [f.split('_')[-2] for f in results]
        except:
            print(f'[FAIL] {tool} {case}: Cannot extract model name from filenames')
            models = []
            continue
        resModels = {}
        for model in models:
            filename = os.path.join(simDir, tool, '_results', case+'_'+model+'_rotor-avg.csv')
            try:
                df = readRotorAvg(filename)
            except Exception as e:
                print(f'[FAIL] {tool} {case} {model}: '+e.args[0])
                continue
            print(f'[ OK ] {tool} {case} {model}')
            resModels[model] = df
        resTools[tool] = resModels
    resCases[case] = resTools


# --- Plot
CASE2KEY={'yaw':'Yaw_[deg]','cone':'Cone_[deg]'}
for case, resTools  in resCases.items():
    key = CASE2KEY[case]

    fig,axes = plt.subplots(1, 2, sharex=True, figsize=(12.8,4.8)) # (6.4,4.8)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.13, hspace=0.05, wspace=0.30)
    for tool, resModels in resTools.items():
        for model, df in resModels.items():
            sty_dict = getStyle(case, tool, model)
            axes[0].plot(df[key], df['Power_[W]'] , label=f'{tool}-{model}', **sty_dict)
            axes[1].plot(df[key], df['Thrust_[N]'], label=f'{tool}-{model}', **sty_dict)

    axes[0].set_ylabel('Power [W]')
    axes[0].set_xlabel(key.replace('_',' '))
    axes[0].legend()      

    axes[1].set_ylabel('Thrust [N]')
    axes[1].set_xlabel(key.replace('_',' '))

plt.show()
