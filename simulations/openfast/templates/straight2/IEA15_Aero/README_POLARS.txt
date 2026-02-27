

R= 1.170290154583781e+02
grid =np.array([0.0 , 0.02     , 0.15           , 0.24517031675566095 , 0.3288439506472435 , 0.4391793464459161 , 0.5376714071084352 , 0.6382076569163737 , 0.7717438522715817 , 1.0])
r =grid*R

labels= [circular  , circular   , SNL-FFA-W3-500 , FFA-W3-360  , FFA-W3-330blend , FFA-W3-301  , FFA-W3-270blend , FFA-W3-241  , FFA-W3-211  , FFA-W3-211]
r = np.array([  0. , 2.34058031 , 17.55435232    , 28.69204079 , 38.48428378     , 51.39672652 , 62.92315541     , 74.68881375 , 90.31642322 , 117.02901546])

#  --- Indices based on 30 spanwise stations
#   0   i=1   circular  - relthick 1
#   5   i=6-  SNL-FFA-W3-500 - relthick 0.5
#   8   i=9-  FFA-W3-360 relative_thickness: 0.36
#  10   i=11- FFA-W3-330blend - rel thick 0.33
#  13   i=14- FFA-W3-301 relative_thickness: 0.301
#  16   i=17- FFA-W3-270blend rel thick 0.27
#  19   i=20- FFA-W3-241 rel thick 0.241
#  23   i=24- FFA-W3-211  rel thick 0.211
