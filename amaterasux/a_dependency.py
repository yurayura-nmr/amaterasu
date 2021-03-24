import imp
import subprocess
import sys

from a_cout import *

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def checkModule(module):
    try:
        imp.find_module(module)
        nprint("Checking for python module: " + module, "... found.")
    except ImportError:
        nprint("Checking for python module:" + module, "... MISSING.")
        sys.exit()

def checkCommand(cmd):
    if cmd_exists(cmd) is True:
        nprint("Checking for executable:" + cmd, "... found.")
    elif cmd_exists(cmd) is False:
        nprint("Checking for executable:" + cmd, "... MISSING.")
        sys.exit()

def checkModules():
    nprint("Checking if required modules are installed", "")
    checkModule('numpy')
    checkModule('scipy')
    checkModule('nmrglue')

    import nmrglue
    if nmrglue.__version__ < 0.6:
        err("nmrglue version found is too low. Version 0.6 or higher is required. Please see INSTALL.txt for instructions how to install nmrglue.")
    else:
        # actually, it seems that ONLY 0.6 works for me. 0.7-dev for example throws an error.
        nprint("[Warning]", "nmrglue higher than required version 0.6 detected. 0.6 works best. Errors happen for 0.7-dev. In these cases, downgrade to 0.6")
        pass

    checkCommand('csh')
    checkCommand('nmrWish')
    checkCommand('mplot')
    checkCommand('glove')
    checkCommand('r1rho2glove')
