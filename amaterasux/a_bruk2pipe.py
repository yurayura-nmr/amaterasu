import os
from a_cout import *


def makeFidCom(experiment):
    """
    Make fid.com file (Bruker to nmrPipe conversion)
    """

    fidCom = ('#!/bin/csh\n' +
              r'bruk2pipe -in ./ser \
-bad 0.0 -aswap -DMX -decim DECIM -dspfvs DSPFVS -grpdly GRPDLY  \
-xN              _TD_  -yN                TN  -aN               VAL  -zN               TD4  \
-xT               _RL  -yT                RN  -aT               VAL  -zT               TD4  \
-xMODE            DQD  -yMODE  Echo-AntiEcho  -aMODE           Real  -zMODE           Real  \
-xSW         __SW_h__  -ySW            _SW_n  -aSW             21.0  -zSW              TD4  \
-xOBS        __SFO1__  -yOBS        __SFO3__  -aOBS               1  -zOBS               1  \
-xCAR           4.700  -yCAR       ____wN___  -aCAR             0.0  -zCAR             0.0  \
-xLAB              HN  -yLAB             15N  -aLAB             TAU  -zLAB              ID  \
-ndim               4  -aq2D          States                                                \
| pipe2xyz -out ./fid/%d.fid -verb -ov' + '\n')

    """
    In the pseudo-4D acquisition mode currently implemented, the 15N offset is arbitrary.
    Here, we simply set the offset to 100 ppm.
    """

    experiment.wN = 100.00

    fidCom = fidCom.replace('DECIM',     str(experiment.decim))
    fidCom = fidCom.replace('DSPFVS',    str(experiment.dspfvs))
    fidCom = fidCom.replace('GRPDLY',    str(experiment.grpdly))
    fidCom = fidCom.replace('_TD_',      str(experiment.TD))
    fidCom = fidCom.replace('_RL',       str(experiment.TD / 2))
    fidCom = fidCom.replace('TN',        str(experiment.TDn))

    fidCom = fidCom.replace('RN', ' ' + str(experiment.TDn / 2))
    fidCom = fidCom.replace('__SW_h__',  str(round(experiment.SW_h, 3)))
    fidCom = fidCom.replace('_SW_n',     str(round(experiment.SW_n, 3)))
    fidCom = fidCom.replace('__SFO1__',  str(round(experiment.SFO1, 4)))
    fidCom = fidCom.replace('__SFO3__',  str(round(experiment.SFO3, 5)))
    fidCom = fidCom.replace('____wN___', str(round(experiment.wN, 5)))
    fidCom = fidCom.replace('VAL',       str(len(experiment.valist)))

    """
    The number of points in the pseudo (4th) dimension is obtained from the acqu4s file. 
    """
    fidCom = fidCom.replace('TD4',       str(experiment.TD4))

    experiment.fidComString = fidCom


def fidCom(experiment):
    """
    Make and execute fid.com in reference or data directory
    Stay in the directory for the next step.
    """

    nprint('CONVERT', 'Bruker ---> nmrPipe format')

    os.chdir(experiment.dataDir)
    fidComString = experiment.fidComString

    f = open('./fid.com', 'w')
    f.write(fidComString)
    f.close()

    os.system("chmod +x fid.com")
    os.system("./fid.com")

    try:
        os.chdir('fid')
    except OSError:
        err("Could not enter fid directory. Probably conversion to nmrPipe format did not work.")
