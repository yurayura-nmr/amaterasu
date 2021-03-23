global tclfile

tclfile = r"""#!/bin/sh
# The next line restarts using nmrWish \
exec nmrWish "$0" -- "$@" -notk

set tabName  test.tab
set specName test.ft
set tabCount 1

set tabDir [file dirname $tabName]

if {![file exists $tabDir]} {file mkdir $tabDir}


set thisSpecName $specName
set thisTabName  $tabName

set x1      1
set xN      $$$$
set xInc    $$$$
set xExtra  2
set xLast   [expr $xN + $xExtra + 1]

set y1      1
set yN      128
set yInc    128
set yExtra  2
set yLast   [expr $yN + $yExtra + 1]

    set yFirst  $y1

while {$yFirst <= 1 + $yN - $yExtra} \
   {
    set yNext [expr $yFirst+$yInc+2*$yExtra-1]
    if {$yNext > $yLast} {set yNext $yLast}

    set xFirst  $x1

while {$xFirst <= 1 + $xN - $xExtra} \
   {
    set xNext [expr $xFirst+$xInc+2*$xExtra-1]
    if {$xNext > $xLast} {set xNext $xLast}

    readROI -roi 1 \
       -ndim 2 -in $thisSpecName \
       -x X_AXIS $xFirst $xNext           \
       -y Y_AXIS $yFirst $yNext           \
       -verb

    pkFindROI -roi 1 \
      -sigma 2669.02 -pChi 0.0001 -plus 45067.1 -minus -45067.1 \
      -dx        2     2 \
      -idx       2     2 \
      -tol    8.00  8.00 \
      -hiAdj  1.20  1.80 \
      -lw    15.00  0.00 \
       -sinc -mask -out $thisTabName -verb

    set xFirst [expr 1 + $xNext - 2*$xExtra]
   }
    set yFirst [expr 1 + $yNext - 2*$yExtra]
   }

exit

"""

def makePeakPickTcl(args, experiment):
    """
    Using NMRPipe for peak picking.
    Fill into the template script the region of interest
    (ROI) based on ZF and TD (amide region is approx. 0.37 * TD)
    Adjust by division by 2
    """
    ROI = experiment.ROI

    foldername = experiment.dataDir

    tclout = tclfile.replace('$$$$', str(ROI))

    with open(foldername + "/fid/pk.tcl", "wt") as fout:
        fout.write(tclout)
