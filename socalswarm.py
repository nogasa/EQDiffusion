import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
import random
import xlrd
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

# Pull data
catalog.harvest_xyz('./data/forandy/xyz_10')
for date in catalog.Decimal_dates:
    catalog.relative_decimal_dates.append(date - min(catalog.Decimal_dates))

# Determine first quake of the swarm
min_time = min(catalog.Decimal_dates)
min_index = catalog.Decimal_dates.index(min_time)

# Determine mapping boundaries
catalog.minlat = min(catalog.Lats)
catalog.maxlat = max(catalog.Lats)
catalog.minlon = min(catalog.Lons)
catalog.maxlon = max(catalog.Lons)
londist = catalog.maxlon - catalog.minlon
latdist = catalog.maxlat - catalog.minlat

# Determine relative distances between all events and first event
i=0
for event in catalog.Decimal_dates:
    lon1, lat1, lon2, lat2 = map(radians, [catalog.Lons[min_index], catalog.Lats[min_index],
                                           catalog.Lons[i], catalog.Lats[i]])
    km = mf.haversine_distance(lon1,lat1,lon2,lat2)
    catalog.Relative_distances.append(km)
    i=i+1

# Generate curve for plotting
num_intervals = 20.
dmaxima, tmaxima = catalog.find_maxima(num_intervals)             # finds the max value in each time interval
for value in dmaxima:                                  # square each distance value
    d = value**2
    catalog.r.append(d)
catalog.t = tmaxima                                    # establishes t array from the maxima array
catalog.t = np.asmatrix(catalog.t)                     # convert t array to t matrix
catalog.t = catalog.t.T                                # transpose t matrix into 1 column t matrix
catalog.r = np.asmatrix(catalog.r)                     # convert r array to r matrix
catalog.r = catalog.r.T                                # transpose r matrix into 1 column r matrix

# LEAST SQUARES SOLUTION via STATSMODELS
mod_wls = sm.WLS(catalog.r, catalog.t)
res_wls = mod_wls.fit()
catalog.D = res_wls.params
catalog.D_err = res_wls.bse

# Printing routine
print 'r:'
print catalog.r
print 't:'
print catalog.t
print 'D:'
print catalog.D
print 'standard error:'
print catalog.D_err

# Generate points to be used to plot curve
groups = 500.
t1 = np.asmatrix(np.linspace(0.,max(catalog.relative_decimal_dates), groups))        # Generate evenly spaced time values
t1 = t1.T                   # transpose into 1 column matrix
r1 = t1 * catalog.D         # multiply to get theoretical squareddistance values
r1 = np.sqrt(r1)            # root to get true distance values

# Generate y-coordinates for confidence intervals
r2 = np.sqrt(t1 * (catalog.D + catalog.D_err))
r3 = np.sqrt(t1 * (catalog.D - catalog.D_err))
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

# Generate curve to be plotted
x = np.array(np.linspace(0.,max(catalog.relative_decimal_dates),groups))       # Generate x values for curve
r1 = r1.T                                                                      # Generate y values for curve
r1 = np.array(r1)
y=[]
for value in np.ndenumerate(r1):
    y.append(value[1])
y = np.array(y)

# Curvey fitting using STATSMODELS.OLS
mod_ols = sm.OLS(y,x)
res_ols = mod_ols.fit()

# Plot map view
point_color = 'lightblue'
mappy = False
if mappy == True:
    geomap = plt.figure()
    ax1 = plt.axes([0.075, 0.01, 0.875, 0.975])
    map = Basemap(llcrnrlon=catalog.minlon -.10 ,llcrnrlat=catalog.minlat-.10,urcrnrlon=catalog.maxlon+.10,
        urcrnrlat=catalog.maxlat+.10, epsg=4269, projection='tmerc')
    map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2500,dpi=150, verbose= True, ax=ax1)
    ax1.set_alpha(0.5)
    parallels = np.arange(round(catalog.minlat),round(catalog.maxlat,1),0.05)
    map.drawparallels(parallels,labels=[True, False, False, False],linewidth=0)
    meridians = np.arange(round(catalog.minlon,1),round(catalog.maxlon,1),0.05)
    map.drawmeridians(meridians,labels=[False, False, False, True],linewidth=0)
    ax1.scatter(catalog.Lons, catalog.Lats, color = point_color, zorder = 11)
    plt.title('SOCAL EARTHQUAKE SWARM', fontweight='bold')
    # Plot patch representing sampling area
    x1, y1 = map(catalog.minlon, catalog.maxlat)
    x2, y2 = map(catalog.minlon, catalog.minlat)
    x3, y3 = map(catalog.maxlon, catalog.minlat)
    x4, y4 = map(catalog.maxlon, catalog.maxlat)
    poly = Polygon([(x1,y1), (x2,y2), (x3,y3), (x4,y4)], alpha = 0.2, facecolor='white', edgecolor='black', zorder=10)
    plt.gca().add_patch(poly)
    plt.show()

plotty = True
if plotty == True:
    # Plot distances vs time
    plt.scatter(catalog.relative_decimal_dates, catalog.Relative_distances, color = point_color, label = 'events')
    plt.scatter(tmaxima, dmaxima, color='blue', label = 'selected events')
    plt.plot(x,y,color='black', label = 'r = sqrt(4piDt)')
    plt.plot(x,Y1, 'black',linestyle='--', label = 'standard error')
    plt.plot(x,Y2, 'black',linestyle='--')
    plt.title('SOCAL EQ Swarm Diffusion')
    plt.ylabel('DISTANCE (KM)')
    plt.xlabel('TIME (DECIMAL YEARS)')
    plt.xlim(min(catalog.relative_decimal_dates),max(catalog.relative_decimal_dates))
    plt.ylim(0., 2.)
    plt.legend()
    plt.show()


