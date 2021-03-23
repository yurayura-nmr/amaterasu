from a_fid import *
from a_cout import *

import sys


def makeFidObjects(residue, experiment):
    """
    Generate FID objects for current residue spin-locked data (usually >19)
    """

    numberFids = len(experiment.fidFilenames)
    fidsPerResidue = len(experiment.valist)

    nprint("Number of residues     ", experiment.TD4)
    nprint("Number of FIDs/residue ", fidsPerResidue)
    nprint("Total number of FIDs   ", numberFids)
    nprint("Current residue #      ", residue.index)

    fidObjectsData = list()
    fidObjectsReference = list()

    """
    The first (n-2) experiments are spin-locked
    """

    start = residue.index * fidsPerResidue
    end = start + fidsPerResidue - 2

    for i in range(start, end):
        testFid = fid()
        testFid.index = i
        testFid.filename = experiment.fidFilenames[i]
        testFid.reference = False
        fidObjectsData.append(testFid)
        # print testFid.filename

    #nprint ("Spin-lock FIDs", fidObjectsData)

    """
    The next 2 experiments are reference experiments
    """

    start = residue.index * fidsPerResidue + (len(experiment.valist) - 2)
    end = start + 2

    for i in range(start, end):
        testFid = fid()
        testFid.index = i
        testFid.filename = experiment.fidFilenames[i]
        testFid.reference = True
        fidObjectsReference.append(testFid)

    #nprint ("Reference (or screening) FIDs", fidObjectsReference)

    """
    Store the information in the residue object
    """

    residue.fidObjectsData = fidObjectsData
    residue.fidObjectsReference = fidObjectsReference
