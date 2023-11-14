# AeroBench

Suggested set of simulations for benchmark of wind turbine simulation tools.

Scripts to generate the inputs and postprocess the outputs will be provided.



## Introduction

Multiple cases are defined (more details below):

- `yaw`: a parametric study on the yaw angle
- `cone`: a parametric study on the cone angle


Different kind of outputs are requested. See below. 





### Suggested directory structure:

The plotting scripts will assume a given directory structure to plot the result for different tools, different cases, model, etc.


Note: directories with an underscore are ignored by default in this repository. 
Consider only adding the template files and scripts to generate the input files.



Suggested structure:

```
simulations/[tool]/_results/[case]_[model]_[output].csv
simulations/[tool]/_[case]/[model]/input_file.dat
```

 - With `[case]` in `{yaw, cone}`
 - With `[output]` in `{rotor-avg, rotor-azi, span-avg, station[N]}`
 - With `[tool]` in `{openfast, awsm, bladed, hawc2, etc}` or institution name `{nrel, dtu, tno, dlr, etc.}`
 - With `[model]` in `{bem, fvw, cfd}'` (submodels can be set as follows: `bem-version2`)


Example:
```
simulations/openfast/_results/yaw_bem_rotor.csv
simulations/openfast/_yaw/bem/yaw_-50.0.fst
```




## Conventions


- Blade 1 pointing up, azimuth=0deg
- Cone angle: positive if the blades are coning upstream (Opposite of OpenFAST convention). 
  Blades are coned with respect to the rotor center, not the blade root...
- Yaw angle: "nacelle yaw angle" (not wind yaw), positive about the vertical axis.

The "polar" (or hub/blade1) coordinate system,

- `x_p` is pointing downstream along the rotor axis
- `z_p` is pointing towards the first blade, rotates with the first blade, and remains within the rotor-normal plane. 
- `y_p` is pointing towards the first blade, rotates with the first blade, and remains within the rotor-normal plane.

with origin at the rotor center (but origin is irrelevant).
For a straight blade, the `z_p` axis coincides with the blade and pitch axis.


## Cases

###  baseline simulation setup

IEA15-MW Wind turbine but with the following properties:

- Rigid structure
- Aerodynamic center on pitch axis
- No tilt 
- No precone 
- No prebend
- No presweep 
- Hub Radius=3.97m
- Tip radius=120.99902m
- Overhang = 12.0313m
- Hub Height set to 200m
- 50 equidistant blade stations from 0 to 117.02902m

Baseline condition:

- Wind speed constant and uniform, U0 =9.0273m/s
- Rotational speed, constant, Omega=6.4135rpm. 
- Pitch=0deg 
- No shear
- No tower influence
 


### case: yaw

Baseline setup with yaw angle varied

- yaw :  from -50 to 50 by step of 5 [deg]

### case: cone

- cone:  from -50 to 50 by step of 5 [deg]  # Note: coning happens at rotor center not blade root





## Outputs and results formats


Format specifications:

 - CSV (comma separated) format 
 - `.csv` extension
 - one line of header
 - the header line (also comma separated) defines the column names.
 - Column names include the variable name and the unit in squared brackets
 - But recommended to keep the first column as the "Main variable"


### output: rotor-avg

Rotor integral quantities, averaged over one rotor revolution (assuming the solution has reached a periodic steady state).
Columns: 
```
[PARAMETRIC_VARIABLE], Power_[W], Thrust_[N], more
```

Example, for the yaw case:
Columns: 
```
Yaw_[deg], Power_[W], Thrust_[N]
```

TODO more columns to be added.



### output: rotor-azi

Rotor integral quantities, bin averaged as function of azimuth (e.g. 60 bins, to be determined later). The values for each case are (row-)concatenated in the same file.
Columns: 
```
Azimuth_[deg], [PARAMETRIC_VARIABLE], [Same columns as the rotor-avg case]
```


### output: span-avg

Blade 1, spanwise quantities, averaged over one rotor revolution.
Columns (split on several lines for readability):

```
r_[m], 
Fn_[N/m], Ft_[N/m], 
Vdisxp_[m/s], Vdisyp_[m/s], Vdisyp_[m/s], 
Vindxp_[m/s], Vindyp_[m/s], Vindyp_[m/s]
```

with: 

 - `r`: distance from blade root
 - `Fn`: force per length normal to chord
 - `Ft`: force per length tangential to chord (sign TBD)
 - `Vdis*p`: Disturbed velocity (free stream + tower influence) in polar coordinate system at given radial location
 - `Vind*p`: Induced velocity at aerodynamic center in polar coordinate system at given radial location
 - TODO More columns to come


### output: station[N]

Blade 1 outputs, at a given radial position, bin-averaged as function of azimuth. `N` represents the node index (assuming 50 sections) such that:

- N=10,  1.772839218313782e-01m (from blade root, node 10)
- N=20,  1.961491644965832e-01m (node 20)
- N=30, -4.485233220920201e-01m (node 30)
- N=40, -1.913679799182830e+00m (node 40)
- N=45, -2.871202075032245e+00m (node 45)


For a given case, results from the different simulations are row-concatenanted into one output file.
Columns: 
```
Azimuth_[deg], [PARAMETRIC_VARIABLE], [same columns as span-avg]
```

