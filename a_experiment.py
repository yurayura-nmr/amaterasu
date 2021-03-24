from nmrglue import fileio
from numpy import log10

from a_readfile import *
from a_dbhz import *
from a_bruk2pipe import *
from a_sortfids import *
from a_cout import *
from a_residue import *


class experiment:

    def __init__(self):
        self.screeningThreshold = 0.95
        self.dataDir = ''
        self.p0 = 'auto'
        self.p1 = 'auto'

    def readParameters(self, args):
        """
        Read acquisition parameters from Bruker acqus files.
        Store in residue object.
        """

        try:
            dic, data = fileio.bruker.read(self.dataDir)
        except IOError:
            err("Could not find data directory")

        """
        General acquisition parameters
        """

        self.decim = int(dic['acqus']['DECIM'])
        self.dspfvs = int(dic['acqus']['DSPFVS'])
        self.grpdly = float(dic['acqus']['GRPDLY'])

        """
        Sweep width, time domain, frequencies
        """

        self.SW_h = float(dic['acqus']['SW_h'])
        self.SW_n = float(dic['acqu2s']['SW_h'])
        self.TE = float(dic['acqus']['TE'])
        self.TD = int(dic['acqus']['TD'])
        self.TDn = int(dic['acqu2s']['TD'])
        self.TD4 = int(dic['acqu4s']['TD'])
        self.BF3 = float(dic['acqus']['BF3'])
        self.O3 = float(dic['acqus']['O3'])
        self.SFO1 = float(dic['acqus']['SFO1'])
        self.SFO3 = float(dic['acqus']['SFO3'])

        """
        15N hard pulse and spinlock pulse length and power.
        """

        self.N15pulseLength = float(dic['acqus']['P'][21])
        self.N15pulseWatt = float(dic['acqus']['PLW'][3])
        self.spinLockLength = float(dic['acqus']['P'][25]) / 1E6

        """
        Convert W to dB
        """

        self.N15pulseDB = -10 * log10(self.N15pulseWatt)

        """
        Determine region of interest
        """

        self.ROI = int(self.TD * 0.37 * 8)       # 8 = 2 * 4 ZF

        """
        Debug
        #self.ROI = int(self.TD * 0.37 * 4)       # debug
        #nprint("TD",  self.TD)
        #nprint("ROI", self.ROI)
        """

        """
        Read valist
        """

        self.readValist(args)

        """
        Read fq3list
        """
        if args.off:
            self.readFq3list(args)

        """
        Prepare fid.com
        """

        makeFidCom(self)

        """
        Read the filenames of the fid files
        """

        self.readFidFilenames()

        """
        Read fq1list, fq2list
        Strip header (ppm / bf)
        """

        fq1list = readFile(self.dataDir + "/fq1list")
        fq2list = readFile(self.dataDir + "/fq2list")

        self.fq1list = fq1list[1:]
        self.fq2list = fq2list[1:]

    def readValist(self, args):
        """
        Read valist (Spin-lock power values [dB])
        Delete first line "dB" if existing
        Remove heating compensation entries
        Convert power values from dB to Hz
        """

        filename = self.dataDir + '/valist'

        valist = readFile(filename)

        if str(valist[0][0]) == 'dB':
            del valist[0]

        valist = valist[1::2]

        self.valist = dBtoHz(self, valist)

    def readFq3list(self, args):
        """
        Read fq3list (Spin-lock offset values [Hz])
        Delete first line "hz sfo" if existing
        Remove heating compensation entries
        Convert power values from dB to Hz
        """

        filename = self.dataDir + '/fq3list'

        fq3list = readFile(filename)

        #if str(fq3list[0][0]) == 'hz sfo':
        del fq3list[0]

        self.fq3list = fq3list

    def readFidFilenames(self):
        """
        Execute fid.com in data directory
        Read fid filenames
        Sort fid filenames
        Go back to original directory.
        """

        fidFilenames = []

        fidCom(self)

        for i in sorted(os.listdir(os.getcwd())):
            if i.endswith(".fid"):
                fidFilenames.append(i)

        fidFilenames = correctNumbering(self, fidFilenames)

        self.fidFilenames = fidFilenames

        os.chdir('../..')

    def makeResidueObjects(self):
        """
        The pseudo-4D experiment contains many residues.
        Each residue (= resonance or peak) has its own object.
        There are as many residues as entries in the fq1list/fq2list files.

        The objects are combined in the [array] experiment.residues
        """

        numberResidues = len(self.fq1list)

        self.residues = []

        for i in range(numberResidues):
            a = residue()

            a.index = i
            a.wH = float(self.fq1list[i][0])
            a.wN = float(self.fq2list[i][0])

            self.residues.append(a)
