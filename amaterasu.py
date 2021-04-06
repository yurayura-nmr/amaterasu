#!/usr/bin/env python2.7

"""
Amaterasu

Pseudo-4D pulseprogram version; using Python2.7

Erik Walinda
Kyoto University
Graduate School of Medicine

Last change: 2021-3-23

****************** Example Command Line *****************  
********************* For Screening *********************  

./amaterasu.py --data=demo_screening -r -s

--data=1001         [screening data] directory. 
-r                  run
-s                  perform screening
-m                  manual phase information

************** For full dataset processing **************  

./amaterasu.py --data=demo_full -m --p0=0 -r

--data=demo_full    [data] directory
-r                  run
-m                  manual phase information

********** For full off-resonance R1rho data ************  

./amaterasu.py --data=demo_offres -m --p0=0 -r -off

--data=demo_offres  [data] directory
-r                  run
-m                  manual phase information

*********************************************************
"""

from amaterasux import *

amaterasux.main()
