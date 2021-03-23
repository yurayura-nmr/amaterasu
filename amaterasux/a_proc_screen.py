from a_pipe_peakpick import *
from a_make_fidobjects import *
from a_cout import *
from a_ft import *
from a_getintensity import *
from a_output import *
from a_phase import *

import sys


def screenResidue(residue, args, experiment):
    """
    Process the dataset with its corresponding reference dataset.
    Using manual or automatic phase correction
    """

    makePeakPickTcl(args, experiment)
    makeFidObjects(residue, experiment)

    if args.m:
        residue.p0 = args.p0
        residue.p1 = 0
        nprint("User-specified phase [p0]", str(residue.p0))
    else:
        nprint("Automatic phasing", '[p0] [p1]')
        residue = phaseReference(residue, experiment)

    """
    Fourier Transform all FIDs
    Currently Amaterasu treats the screening FIDs internally as "reference".
    """

    ftAllRef(residue, args, experiment)

    """
    Get intensities for all peaks in the spectra
    """

    getIntAllRef(residue, args, experiment)
