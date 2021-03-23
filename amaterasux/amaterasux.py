from a_argparse import *
from a_processdata import *
from a_dependency import *

def main():
    """
    Check command line arguments and if no problems, start.
    """
    args = parseArguments()
    processData(args)

checkModules()
main()
