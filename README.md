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
[tool]/_results/[case]_[model]_[output].csv
[tool]/_[case]/[model]/input_file.dat
```

 - With `[case]` in `{yaw, cone}`
 - With `[output]` in `{rotor-avg, rotor-azi, span-avg, station[N]}`
 - With `[tool]` in `{openfast, awsm, bladed, hawc2, etc}`
 - With `[model]` in `{bem, fvw, cfd}'` (submodels can be set as follows: `bem-version2`)


Example:
```
openfast/_results/yaw_bem_rotor.csv
openfast/_yaw/bem/yaw_-50.0.fst
```




## Conventions


- Blade 1 pointing up, azimuth=0deg
- Cone angle: positive if the blades are coning upstream (Opposite of OpenFAST convention). 
  Blades are coned with respect to the rotor center, not the blade root...
- Yaw angle: "nacelle yaw angle" (not wind yaw), positive about the vertical axis.



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
- 51 equidistant blade stations from 0 to 117.02902m

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

```
Columns: [PARAMETRIC_VARIABLE], Power_[W], Thrust_[N], more
```

Example, for the yaw case:

```
Columns: Yaw_[deg], Power_[W], Thrust_[N]
```

TODO more columns to be added.



### output: rotor-azi

Rotor integral quantities, bin averaged as function of azimuth (e.g. 60 bins, to be determined later). The values for each case are (row-)concatenated in the same file.

```
Columns: Azimuth_[deg], [PARAMETRIC_VARIABLE], Power_[W], Thrust_[N]
```

TODO More on that and example.


### output: span-avg

Blade 1, spanwise quantities, averaged over one rotor revolution.


```
Columns: r_[m], Fn_[N/m], Ft_[N/m], more
```

with: 

 - r: distance from blade root
 - Fn: force per length normal to chord
 - Ft: force per length tangential to chord (sign TBD)
 - TODO More columns to come


### output: station[N]

Blade 1 outputs, at a given radial position, bin-averaged as function of azimuth. `N` represents an index such that:

- N=1, r=21.06522278250806m  (from blade root, node 10)
- N=2, r=44.471025874183674m (node 20)
- N=3, r=67.87682896585929m  (node 30)
- N=4, r=91.28263205753491m  (node 40)
- N=5, r=114.68843514921053  (node 50)

For a given case, results from the different simulations are row-concatenanted into one output file.

```
Columns: Azimuth_[deg], [PARAMETRIC_VARIABLE], Fn_[N/m], Ft_[N/m], more
```

TODO: more columns
