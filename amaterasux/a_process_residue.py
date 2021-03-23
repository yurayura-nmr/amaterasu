from a_pipe_peakpick import *
from a_make_fidobjects import *
from a_ft import *
from a_phase import *
from a_getintensity import *
from a_output import *

import sys


def processResidue(residue, args, experiment):
    """
    Process the dataset with its corresponding reference dataset.
    Using manual or automatic phase correction
    For automatic phase correction: determine ref. p0, p1 from 1D projection        
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
    """

    ftAllRef(residue, args, experiment)
    ftAll(residue, args, experiment)

    """
    Get intensities for all peaks in the spectra
    """

    getIntAllRef(residue, args, experiment)
    getIntAll(residue, args, experiment)

    """
    If this is the first residue processed, write the header of the output intensity file.
    """

    if residue.index == 0:
        writeIntFileHeader(residue, experiment)

    writeIntFileLine(residue, experiment)
