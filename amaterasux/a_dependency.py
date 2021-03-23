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
        pass

    checkCommand('csh')
    checkCommand('nmrWish')
    checkCommand('mplot')
    checkCommand('glove')
    checkCommand('r1rho2glove')
