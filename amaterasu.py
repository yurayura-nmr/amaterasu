#!/usr/bin/env python2.7

"""
Amaterasu'Kai

Pseudo-4D pulseprogram version; using Python2.7

Erik Walinda
Kyoto University
Graduate School of Medicine

Last change: 2021-3-23

****************** Example Command Line *****************  
********************* For Screening *********************  

./amaterasu.py --data=demo_screening -r -s

--data=1001       [screening data] directory. 
-r                run
-s                perform screening

************** For full dataset processing **************  

./amaterasu.py --data=demo_full -m --p0=0 -r

--data=1000       [data] directory
-r                run

*********************************************************
"""

from amaterasux import *

amaterasux.main()