import os

NwCP = 40
HwCP = NwCP

"""
Creates input scripts and calls SIMPSON to simulate the CP excitation pulse sequence on a user-chosen grid.
Requires aru_tmp.tcl.
"""

# offsets
__OH__ = 1
__ON__ = 1        
maxTr = 0.0108    # max transfer time

def prepareFile(__ON__, __OH__):
    with open("aru_run.tcl", "wt") as fout:
        with open("aru_tmp.tcl", "rt") as fin:
            for line in fin:
                a = line.replace('__NwCP__', str(NwCP))
                a = a.replace('__HwCP__', str(HwCP))
                a = a.replace('__ON__', str(__ON__))
                a = a.replace('__OH__', str(__OH__))
                fout.write(a)

def getSx(maxTr):
    os.system("simpson ./aru_run.tcl")
    with open("trial.txt", "rt") as fin:
        for line in fin:
            columns = line.split()
            if columns[0] == str(maxTr):
                Sx = columns[1]
    return Sx


matrix = []

jiku = range(-405, 405)

for Noffset in jiku:
     for Hoffset in jiku:
         prepareFile(Noffset, Hoffset)
         Sx = getSx(maxTr)
         print "Noffset: ", Noffset, "\t Hoffset:", Hoffset
         matrix.append([Noffset, Hoffset, Sx])

outfile = str(NwCP) + "_matrix.txt"

with open(outfile, "wt") as fout:
    for i in matrix:
        fout.write(str(i[0]).ljust(20) + str(i[1]).ljust(20) + str(i[2]))
        fout.write("\n")
