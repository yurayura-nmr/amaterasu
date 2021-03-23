import sys

def err(message):
    """
    Prints error message and terminates the program.
    """
    nprint('ERROR', message)
    sys.exit()

def nprint(a, b):
    """
    Left-aligned command line output.
    """
    print "" + str(a).ljust(40) + str(b).ljust(60)

def printf(format, *args):
    sys.stdout.write(format % args)

def printParameters(self):
    """
    Show the parameters for the Amaterasu run.
    """
    nprint("\nAcquisition Parameters \n", "")
    nprint("Data directory", self.dataDir)

    nprint("15N hard pulse power  [dB]", self.N15pulseDB)
    nprint("15N hard pulse length [dB]", self.N15pulseLength)
    nprint("15N spinlock length   [dB]", self.spinLockLength)
