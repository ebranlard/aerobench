import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
# Local 
import welib.weio as weio
import welib.fast.fastlib as fastlib
from welib.tools.curve_fitting import model_fit

scriptDir=os.path.dirname(__file__)

# TODO
KEYS={'shear':'ShearExp_[-]','cone':'Cone_[deg]','tilt':'Tilt_[deg]','bend':'PrebendTipAngle_[deg]','sweep':'PresweepTipAngle_[deg]','yaw':'Yaw_[deg]','mixy':'Yaw_[deg]'}
ALGOS=['bem', 'olf']

def getSimParams():
    r_hub   = 3.970000
    R_blade = 117.0290154583781
    R       = r_hub + R_blade
    rho     = 1.225
    U0      = 9.0273
    RPM     = 6.4135 
    return R, R_blade, rho, U0, RPM

def num2str(n,fmt='{:02d}'):
    if n<0:
        s = 'm'+(fmt.format(-n)).strip()
    else:
        s = 'p'+(fmt.format(n)).strip()
    return s


# --------------------------------------------------------------------------------}
# --- File creation 
# --------------------------------------------------------------------------------{
def generate(runDir, main_file, exe, old=False, proj=None, var=None, varname='Precone(1)', bemmod=None, dirs=None):
    templateDir = os.path.dirname(main_file)
    main_file   = os.path.basename(main_file)
    print(runDir)
    dirs.append(runDir)
    PARAMS=[]
    for c in var:
        p=dict()
        p[varname] = c
        if varname=='PLExp':
            c=int(c*100)
        if c>=0:
            p['__name__'] = 'ad_driver_p{:02d}'.format(c)
        else:
            p['__name__'] = 'ad_driver_m{:02d}'.format(-c)

        if old:
            p['OutFileRoot'] = p['__name__']
        if proj is not None:
            p['ProjMod(1)'] = proj
        if bemmod is not None:
            p['BEM_Mod(1)'] = bemmod
        PARAMS.append(p)

    files = fastlib.templateReplace(PARAMS, templateDir, outputDir=runDir, main_file=main_file, removeAllowed=False)

    fastlib.runner.writeBatch(os.path.join(runDir,'_RUN_ALL.bat'), files, fastExe=exe)

def generateYaw(runDir, main_file, exe, old=False, proj=None, var=None, extraDict=None, bemmod=None, dirs=None):
    templateDir = os.path.dirname(main_file)
    main_file   = os.path.basename(main_file)
    print(runDir)
    dirs.append(runDir)
    main_file = os.path.join(templateDir, main_file)
    file_out  = os.path.join(runDir, 'ad_driver_yaw.dvr')
    f = weio.read(main_file)
    if proj is not None:
        f['ProjMod(1)'] =proj
    if bemmod is not None:
        f['BEM_Mod(1)'] = bemmod
    if extraDict is not None:
        for k,v in extraDict.items():
            print('Setting ',k,'to',v)
            f[k]=v
    M0 = f['Cases']
    df0 = f.toDataFrame()
    n = len(var)
    df = pd.concat([df0]*n)
    df['Yaw_[deg]']=var
    f['Cases'] = df.values
    f.write(file_out)

    ad = 'AD.dat'
    fastlib.forceCopyFile(os.path.join(templateDir, ad), os.path.join(runDir, ad))
    ad = 'AD_olaf.dat'
    fastlib.forceCopyFile(os.path.join(templateDir, ad), os.path.join(runDir, ad))
    ad = 'OLAF.dat'
    fastlib.forceCopyFile(os.path.join(templateDir, ad), os.path.join(runDir, ad))

    fastlib.runner.writeBatch(os.path.join(runDir,'_RUN_ALL.bat'), [file_out], fastExe=exe)


def writeBatch(dirs, suff='BEM'):
    mainDir=os.path.dirname(dirs[0])
    batchfile = os.path.join(mainDir, '_RUN_ALL_{}.bat'.format(suff))
    with open(batchfile, 'w') as f:
        for d in dirs:
            d2 = os.path.relpath(d, mainDir)
            f.write('cd {} && call _RUN_ALL.bat && cd ..\n'.format(d2))



# --------------------------------------------------------------------------------}
# --- Pospro 
# --------------------------------------------------------------------------------{
def extract(runDir, suffix='', ext='.outb', varname='Cone_[deg]', var=None, avg='wnd', preext='.1'):

    R, R_blade, rho, U0, RPM = getSimParams()

    filenames=[]
    if varname=='PresweepTipAngle_[deg]':
        label='_sweep'
    else:
        label=''
    for c in var:
        if c>=0:
            filename=os.path.join(scriptDir,runDir, 'ad_driver{}_p{:02d}'.format(label,  c) +suffix)
        else:
            filename=os.path.join(scriptDir,runDir, 'ad_driver{}_m{:02d}'.format(label, -c)+suffix)
        filename =filename + preext + ext
        filenames.append(filename)
    try:
        if avg=='wnd':
            df = fastlib.averagePostPro(filenames, avgMethod='constantwindow', avgParam=2, ColMap=None,ColKeep=None, ColSort=None, stats=['mean'])
        else:
            df = fastlib.averagePostPro(filenames, avgMethod='periods', avgParam=1, ColMap=None,ColKeep=None, ColSort=None, stats=['mean'])
    except:
        import pdb; pdb.set_trace()
        print('>>> FAILED TO LOAD', runDir)
        return None
    df.insert(0,varname, var)
    df.sort_values([varname],inplace=True,ascending=True)
    df.reset_index(drop=True,inplace=True) 
    if varname=='PrebendTipAngle_[deg]':
        A = np.pi*(R/np.cos(var*np.pi/180))**2 # <<<<<<<<<
    elif varname=='PrebendSweepAngle_[deg]':
        print('>>> Area presweep')
        A = np.pi*R**2 
    else:
        A = np.pi*(R*np.cos(var*np.pi/180))**2 # <<<<<<<<<
    df['Area'] = A
    try:
        df['RtFldPwr_[W]'] = df['RtAeroPwr_[W]']
        df['RtFldFxh_[N]'] = df['RtAeroFxh_[N]']
    except:
        pass
    df['CP'] = df['RtFldPwr_[W]'] / (1/2*rho*U0**3 *A )
    df['CT'] = df['RtFldFxh_[N]'] / (1/2*rho*U0**2 *A )
    return df


def extractYaw(runDir, suffix='', ext='.outb', var=None):
    R, R_blade, rho, U0, RPM = getSimParams()
    if var is None:
        yaw = np.arange(-50,51,5)
    filenames=[]
    for i,y in enumerate(var):
        filename=os.path.join(scriptDir, runDir, 'ad_driver_yaw.{:d}'.format(i+1)+ext)
        filenames.append(filename)
    try:
        df = fastlib.averagePostPro(filenames, avgMethod='periods', avgParam=1, ColMap=None,ColKeep=None, ColSort='Yaw_[deg]', stats=['mean'])
    except:
        print('>>> FAILED TO LOAD', runDir)
        return None
    A = np.pi*(R*np.cos(0*np.pi/180))**2
    df['Area'] = A
    try:
        df['RtFldPwr_[W]'] = df['RtAeroPwr_[W]']
        df['RtFldFxh_[N]'] = df['RtAeroFxh_[N]']
    except:
        pass
    df['CP'] = df['RtFldPwr_[W]'] / (1/2*rho*U0**3 *A )
    df['CT'] = df['RtFldFxh_[N]'] / (1/2*rho*U0**2 *A )
    return df



# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def postpro(study, var, algos=None):
    if algos is None:
        algos = ALGOS
    sims={}
    print('--------------- {} ----------------'.format(study))
    if study=='cone':
        for algo in algos:
            sims[algo] = extract(runDir='_{}/{}/'.format(study,algo), ext='.outb', varname=KEYS[study], var=var)
    elif study=='yaw':
        for algo in algos:
            sims[algo] = extractYaw(runDir='_{}/{}/'.format(study,algo), ext='.outb', var=var)
    else:
        raise Exception()
    return sims

# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def load_results(studies_names, algos=None):
    """ 
    Load results for a list of studies, and different algorithms
    """
    if not isinstance(studies_names, list):
        studies_names=[studies_names]
    studies={}
    for study in studies_names:
        sims={}
        if algos is None:
            algos = ALGOS
        for model in algos:
            filename = os.path.join(scriptDir,'_results/{}_{}_{}.csv'.format(study,model,output))
            sims[model] = weio.read(filename).toDataFrame()
        studies[study] = sims
    return studies

def significant_digits(df, significance, inplace = False):
    
    # Create a positive data vector with a place holder for NaN / inf data
    data = df.values
    data_positive = np.where(np.isfinite(data) & (data != 0),
                             np.abs(data),
                             10**(significance-1))

    # Align data by magnitude, round, and scale back to original
    magnitude = 10 ** (significance - 1 - np.floor(np.log10(data_positive)))
    data_rounded = np.round(data * magnitude) / magnitude

    # Place back into Series or DataFrame
    if inplace:
        df.loc[:] = data_rounded
    else:
        if isinstance(df, pd.DataFrame):
            return pd.DataFrame(data=data_rounded,
                                index=df.index,
                                columns=df.columns)
        else:
            return pd.Series(data=data_rounded, index=df.index)


def save_results(studies, output='rotor-avg'):
    """ 
    Save results for a list of studies, and different algorithms
    """
    resDir = os.path.join(scriptDir, '_results/')
    if not os.path.exists(resDir):
        os.makedirs(resDir)
    for study in studies.keys():
        sims = studies[study]
        for model in sims.keys():
            df = sims[model]
            if df is not None:
                filename = os.path.join(resDir,'{}_{}_{}.csv'.format(study,model,output))
                print(filename)
                # TODO use col Map
                colKeep = ['Yaw_[deg]', 'RtAeroFxh_[N]', 'RtAeroPwr_[W]']
                colNew  = ['Yaw_[deg]', 'Thrust_[N]' , 'Power_[W]']
                df = pd.DataFrame(data=df[colKeep].values, columns=colNew)
                N = 4
                df = significant_digits(df, N, inplace=False)
                # Convert to string for full control of format output..
                for c in df.columns:
                    if c in ['Yaw_[deg]']:
                        df[c] = df[c].map('{:4.0f}'.format)
                    else:
                        df[c] = df[c].map('{:.3e}'.format)
                df.to_csv(filename, index=False)
                #df.to_csv(filename, index=False, float_format='%.3e')




# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def plot(study, studies, algos, STYs, preffix='', plotType=1, xlim=None, filename=None, alphaBeta=True, extralegend=False):
    # --- 
    sims = studies[study]
    key = KEYS[study]
    # --- 
    if plotType==1:
        # 3x2 plots
        fig,axes = plt.subplots(2, 3, sharex=True, figsize=(15,7.0)) # (6.4,4.8)
        fig.subplots_adjust(left=0.16, right=0.95, top=0.95, bottom=0.11, hspace=0.05, wspace=0.30)
    elif plotType==2:
        fig,axes = plt.subplots(1, 2, sharex=True, figsize=(12.8,4.8)) # (6.4,4.8)
        fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.13, hspace=0.05, wspace=0.30)
    else:
        # 2x2 plots
        fig,axes = plt.subplots(2, 2, sharex=True, figsize=(12.8,6.8)) # (6.4,4.8)
        fig.subplots_adjust(left=0.09, right=0.98, top=0.95, bottom=0.095, hspace=0.18, wspace=0.30)
    for ialgo,algo in enumerate(algos):
        j=0
        df = sims[algo]
        sty = STYs[algo]
        if df is None:
            continue
        # --- HACK
#         if study=='yaw':
#             df.drop(df.head(1).index,inplace=True)
#             df.drop(df.tail(1).index,inplace=True)
            
        val = df[key].values
        i=np.nanargmin(np.abs(val))
        def scale(v):
            return v.values/v.values[i]
        
        if plotType==1 or plotType==3:
            ax=axes[0,j];
            ax.plot(df[key]             , df['RtFldPwr_[W]'] , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
            ax.set_ylabel('Power [W]')
            if extralegend:
                ax.legend()

            ax=axes[1,j];j+=1
            ax.plot(df[key]             , df['RtFldFxh_[N]'] , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
            ax.set_ylabel('Thrust [N]')
            ax.set_xlabel(key.replace('_',' '))
            if extralegend:
                ax.legend()
            
            if plotType==1:
                ax=axes[0,j];
                ax.plot(df[key]             , df['CP']           , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
                ax.set_ylabel(r'$C_P$ [-]')

                ax=axes[1,j];j+=1
                ax.plot(df[key]             , df['CT']           , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
                ax.set_ylabel(r'$C_T$ [-]')
                ax.set_xlabel(key.replace('_',' '))
                ax.legend()      
            
            
            try:
                x = df[key].values
                y = scale(df['CP'])
                y_fit, pfit, fitter = model_fit('eval: cos( (x - {beta})*np.pi/180)**{alpha}', x, y, bounds={'alpha':(-5,5), 'beta':(-5,5)})
                mdl= fitter.model          
                if alphaBeta:
                    lbl=r'$\alpha={:.2f} - \beta={:.1f}$'.format(mdl['coeffs']['alpha'],mdl['coeffs']['beta'])
                else:
                    lbl=r'$\alpha={:.2f}$'.format(mdl['coeffs']['alpha'])
                          
                ax=axes[0,j];
                ax.plot(df[key]             , scale(df['CP']          ) , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=None, lw=sty['lw'])
                ax.plot(df[key]             , mdl['fitted_function'](x   ) , marker='o', ls='' , c=sty['c'] , label=lbl, ms=3)                  
                ax.set_ylabel('$C_P/C_{P,0}$ [-]')
                if alphaBeta:
                    ax.legend(title=r'Fit: $\cos(x-\beta)^\alpha$', fontsize=12) 
                else:
                    ax.legend(title=r'Fit: $\cos(x)^\alpha$', fontsize=12) 
                    
                y = scale(df['CT'])
                y_fit, pfit, fitter = model_fit('eval: cos( (x - {beta})*np.pi/180)**{alpha}', x, y, bounds={'alpha':(-4,4), 'beta':(-5,5)})
                mdl= fitter.model          
                lbl=mdl['formula_num']  
                if alphaBeta:
                    lbl=r'$\alpha={:.2f} - \beta={:.1f}$'.format(mdl['coeffs']['alpha'],mdl['coeffs']['beta'])
                else:
                    lbl=r'$\alpha={:.2f}$'.format(mdl['coeffs']['alpha'])
                
                ax=axes[1,j];j+=1
                ax.plot(df[key]             , scale(df['CT']          ) , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=None, lw=sty['lw'])
                ax.plot(df[key]             , mdl['fitted_function'](x   ) , marker='o', ls='' , c=sty['c'] , label=lbl, ms=3)   
                ax.set_ylabel('$C_T/C_{T,0}$ [-]')      
                ax.set_xlabel(key.replace('_',' '))
                if alphaBeta:
                    ax.legend(title=r'Fit: $\cos(x-\beta)^\alpha$', fontsize=12) 
                else:
                    ax.legend(title=r'Fit: $\cos(x)^\alpha$', fontsize=12) 
            except:
                pass
        else:
            ax=axes[j];j+=1
            ax.plot(df[key]             , df['RtFldPwr_[W]'] , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
            ax.set_ylabel('Power [W]')
            ax.set_xlabel(key.replace('_',' '))
            ax.legend()      
            ax.set_xlim(xlim)

            ax=axes[j];j+=1
            ax.plot(df[key]             , df['RtFldFxh_[N]'] , marker=sty['m'], ls=sty['ls'] , c=sty['c'] , label=sty['label'], lw=sty['lw'])
            ax.set_ylabel('Thrust [N]')
            ax.set_xlabel(key.replace('_',' '))
            ax.legend()      
            ax.set_xlim(xlim)
     
    if plotType==1:
        for ax in axes.flatten():
            ax.grid(True, linestyle=':', lw=0.7, color=(0.6,0.6,0.6))
            ax.tick_params(direction='in', top=True, right=True, labelright=False, labeltop=False, which='both')

    if filename is None:
        figDir = os.path.join(scriptDir, '_figs/')
        if not os.path.exists(figDir):
           os.makedirs(figDir)
        filename = os.path.join(figDir, '{}{}.png'.format(preffix,study))
    else:
        filename+= '{}{}.png'.format(preffix, study)
    dpi=300
    print(filename, dpi)
    fig.savefig(filename, dpi=dpi)

    return fig




