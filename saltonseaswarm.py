import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
import random
import xlrd
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
import plotly.plotly as py
import plotly.graph_objs as go
import pylab as pb
import statsmodels.api as sm
import muffin as mf

# Define catalog
catalog = mf.catalog()
catalog.minyear, catalog.minmonth, catalog.minday = 2016., 9.0, 26.0

# Pull data
catalog.harvest_USGS('./USGSSaltonSeaCatalog2.xls')

# Process data
catalog.glean()

# Establish number of time intervals
num_intervals = 20.

# Find the maximum distances in each time interval, as well as their associated times and mags
dmaxima, tmaxima= catalog.find_maxima(num_intervals)

# Square each distance maxima, build 'r' array to hold maxima (y0 array)
for value in dmaxima:                                  # square each distance value
    d = value**2
    catalog.r.append(d)
catalog.r = np.asmatrix(catalog.r)                     # convert r array to r matrix
catalog.r = catalog.r.T                                # transpose r matrix into 1 column r matrix

# Build 't' array with datetimes of the maximum distances (x0 array)
catalog.t = tmaxima                                    # establishes t array from the maxima array
catalog.t = np.asmatrix(catalog.t)                     # convert t array to t matrix
catalog.t = catalog.t.T                                # transpose t matrix into 1 column t matrix

# Perform least squares solution to determine '4 * pi * D' value
mod_wls = sm.WLS(catalog.r, catalog.t)
res_wls = mod_wls.fit()
catalog.D = res_wls.params
catalog.D_err = res_wls.bse

### PRINTING ROUTINE ###
print 'r:'
print catalog.r
print 't:'
print catalog.t
print 'D:'
print catalog.D
print 'standard error:'
print catalog.D_err
print 'mags'

### MAPPING ROUTINE ####
mappy = False
if mappy == True:
    catalog.cartographer()

### CURVE PLOTTING ROUTINE ###
# Define number of points to plot curve with (go big!)
numb_points = 500.

# Generate new 't' array for plotting of the curve (x array)
t1 = np.asmatrix(np.linspace(0.,max(catalog.relative_decimal_dates), numb_points))
x = t1.T

# Generate new 'r' array for plotting of the curve (y array)
r1 = x * catalog.D         # multiply to get theoretical squared distance values
r1 = np.sqrt(r1)            # root to get true distance values
r1 = r1.T                                                                      # Generate y values for curve
r1 = np.array(r1)
y=[]
for value in np.ndenumerate(r1):
    y.append(value[1])
y = np.array(y)

# Generate y-coordinates for confidence intervals (y1,y2 arrays)
r2 = np.sqrt(x * (catalog.D + catalog.D_err))
r3 = np.sqrt(x * (catalog.D - catalog.D_err))
Y01 = r2.T
Y02 = r3.T
Y01 = np.array(Y01)
Y02 = np.array(Y02)
Y1 = []
Y2 = []
for value in np.ndenumerate(Y01):
    Y1.append(value[1])
for value in np.ndenumerate(Y02):
    Y2.append(value[1])

# Generate grid and contour plot to overlay

plotty = True
if plotty == True:
    # Plot distances vs time
    plt.scatter(catalog.relative_decimal_dates, catalog.Relative_distances, color = 'lightblue', label = 'events')
    plt.scatter(tmaxima, dmaxima, color='blue', label = 'selected events')
    plt.plot(x,y,color='black', label = 'r = sqrt(4piDt)')
    plt.plot(x,Y1, 'black',linestyle='--', label = 'standard error')
    plt.plot(x,Y2, 'black',linestyle='--')
    plt.title('Salton Sea EQ Swarm Diffusion')
    plt.ylabel('DISTANCE (KM)')
    plt.xlabel('TIME (DECIMAL YEARS)')
    plt.xlim(min(catalog.relative_decimal_dates),max(catalog.relative_decimal_dates))
    plt.ylim(0., 2.)
    plt.legend()
    # Generate grid and contour plot to overlay
    z = catalog.Mo
    xi = np.linspace(0., max(catalog.relative_decimal_dates))
    yi = np.linspace(0., max(catalog.Relative_distances))
    zi = griddata((catalog.relative_decimal_dates, catalog.Relative_distances), z,
                  (xi[None, :], yi[:, None]), method='cubic')
    CS = plt.contourf(xi, yi, zi, 15, colors='k')
    CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.viridis)
    CB = plt.colorbar(CS, extend='both')
    # Finish and plot
    plt.show()
