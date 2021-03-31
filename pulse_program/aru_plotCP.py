import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml


def readFile(filename):

    x = []
    y = []
    z = []

    with open(filename, "rt") as infile:
        for line in infile:
            columns = line.split()
            x.append(float(columns[0]))
            y.append(float(columns[1]))
            z.append(float(columns[2]))

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    return x, y, z


np.random.seed(8)
#ndata = 200
#ny, nx = 200, 200
#xmin, xmax = -200, 200
#ymin, ymax = -200, 200

ndata = 400
ny, nx = 400, 400
xmin, xmax = -400, 400
ymin, ymax = -400, 400



x, y, z = readFile("matrix.txt")

xi = np.linspace(xmin, xmax, nx)
yi = np.linspace(ymin, ymax, ny)


# Requires installation of natgrid
# http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/
zi = ml.griddata(x, y, z, xi, yi, interp='nn')

# Or, without natgrid:
# zi = ml.griddata(x, y, z, xi, yi, interp='linear')

fig = plt.figure()

plt.contour(xi, yi, zi, 15, linewidths = 0.5, colors = 'k')
plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
#plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('seismic'))

plt.colorbar() 
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)

fig.savefig("test.pdf")
