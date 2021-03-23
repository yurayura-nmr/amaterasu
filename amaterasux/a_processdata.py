import sys
import a_experiment

from a_cout import *
from a_process_residue import *
from a_proc_screen import *
from a_output import *
from a_output_s import *


def processData(args):
    """
    Check if datadir argument was given 
    """

    if args.dataDir:
        pass
    else:
        err("Data directory not specified.")

    """
    Check if the current experiment is a screening experiment.
    """
    if args.s:
        processScreening(args)
        pass
    else:
        processFull(args)
        pass
    """
    Off-resonance not implemented yet.

    elif args.off:
        #processOffRes(args)     # to do
        pass
    """


def processFull(args):
    """
    Full run
    Make object of type residue.
    Then process this residue.
    """

    experiment = a_experiment.experiment()

    experiment.dataDir = args.dataDir

    experiment.readParameters(args)

    printParameters(experiment)

    experiment.makeResidueObjects()

    """
    Loop over all residues of the current experiment
    Process these residues and call glove to fit the R1rho profile
    """

    for i in experiment.residues:
        currentResidue = i
        processResidue(currentResidue, args, experiment)

    glove(experiment, args)
    sys.exit()


def processScreening(args):
    """
    Screening run
    """

    experiment = a_experiment.experiment()

    experiment.dataDir = args.dataDir

    experiment.readParameters(args)

    printParameters(experiment)

    experiment.makeResidueObjects()

    """
    Loop over all residues of the current experiment
    Process these residues and get the screening intensity ratio
    Write the output as text file 
    """

    for i in experiment.residues:
        currentResidue = i
        screenResidue(currentResidue, args, experiment)

    writeScreeningOutput(experiment)
    sys.exit()
