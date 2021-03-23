from a_argparse import *
from a_processdata import *
from a_dependency import *

def main():
    """
    Go.
    """
    args = parseArguments()
    processData(args)

checkModules()
main()
