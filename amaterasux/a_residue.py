class residue:
    def __init__(self):
        self.wH = 0.00             # CNST1; peak expected from spin-lock selection
        self.wN = 0.00             # O3P;   peak expected from spin-lock selection

        self.wH_observed = 0.00    # peak observed in the experiment (ppm)
        self.index = 0             # position in fq1list
