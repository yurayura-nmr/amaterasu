from argparse import ArgumentParser
import sys

def parseArguments():
    """
    Parse command line arguments.
    """
    parser = ArgumentParser(
        description='Amaterasu | A program to process R1rho relaxation dispersion data')

    parser.add_argument("-r",
                        help="run Amaterasu",
                        action="store_true")

    parser.add_argument("--data",
                        help="[directory] containing the experimental data",
                        dest='dataDir',
                        type=str)

    parser.add_argument("-s",
                        help="experiment is a screening experiment",
                        action="store_true")

    # Off-resonance expt. not yet implemented.
    parser.add_argument("-off",
                        help="experiment is an off-resonance experiment",
                        action="store_true") # testing
   
    parser.add_argument("-m",
                        help="manually apply a first order phase correction; specify with [--p0]",
                        action="store_true")

    parser.add_argument('--p0',
                        action="store",
                        dest="p0",
                        help="first order phase correction value [degrees]",
                        type=float)

    parser.add_argument('--model',
                        action="store",
                        dest="model",
                        help="select theoretical model for R1rho profile fitting. MATRIX, PALMER05, and CONST models are implemented.",
                        type=str)

    args = parser.parse_args()

    if args.r:
        return args
    else:
        sys.exit()
