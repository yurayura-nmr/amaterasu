class fid:

    def __init__(self):
        """
        Parameters describing a given fid or equivalently, the resulting spectrum belonging to
        a certain resonance at a certain spin-lock power or 
                            at a certain spin-lock offset

        Index: e.g. 0 to 24 for 1.fid to 25.fid
        """
        self.reference = False
        self.filename = ''
        self.index = 0
        self.spinlockHz = 0
        self.spinlockOffset = 0 # testing

        """
        Parameters needed to FT the current FID
        """
        self.apodizationOffset = 0.4
        self.apodizationEnd = 0.95
        self.apodizationPower = 1
        self.cValue = 1.0
        self.zeroFilling = 4

        self.tolerance = 0.04
        self.solventFilter = True
