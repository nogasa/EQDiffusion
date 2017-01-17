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
from matplotlib.lines import Line2D
import matplotlib.tri as tri
from mpl_toolkits.basemap import Basemap
import plotly.plotly as py
import plotly.graph_objs as go
import pylab as pb

import muffin as mf

# Define catalog
catalog = mf.catalog()
catalog.minyear, catalog.minmonth, catalog.minday = 1992., 8.0, 1.0
catalog.minlat, catalog.minlon = 35.5, -118.
catalog.maxlat, catalog.maxlon = 36.4, -117
catalog.dlimit = 50.

# Pull data
catalog.harvest_SCDEC('./SCEDCatalog(81-11).txt', boundaries=True)
catalog.tlimit = max(catalog.Times)-min(catalog.Times)
# Determine first quake of the day
min_time = min(catalog.Times)
min_index = catalog.Times.index(min_time)


# Determine relative distances between all events and first event
i=0
for event in catalog.Times:
    lon1, lat1, lon2, lat2 = map(radians, [catalog.Lons[min_index], catalog.Lats[min_index],
                                           catalog.Lons[i], catalog.Lats[i]])
    km = mf.haversine_distance(lon1,lat1,lon2,lat2)
    catalog.Relative_distances.append(km)
    i=i+1

# Generate curve for plotting
groups = 6.                                     # number of time intervals to construct
maxima = catalog.find_maxima(groups)            # finds the max value in each time interval
catalog.t = maxima                              # establishes t array from the maxima array
catalog.r_matrix()                              # generates array of distance values associated with t array

catalog.t = np.asmatrix(catalog.t)              # convert t array to t matrix
catalog.t = catalog.t.T                         # transpose t matrix into 1 column t matrix
catalog.r = np.asmatrix(catalog.r)              # convert r array to r matrix
catalog.r = catalog.r.T                         # transpose r matrix into 1 column r matrix

catalog.D,residuals,rank,s = np.linalg.lstsq(catalog.t,catalog.r)           # LEAST SQUARES OPERATION

# Printing routine
print 'r'
print catalog.r
print 't'
print catalog.t
print 'D'
print catalog.D/4/np.pi

# Generate points to be used to plot curve
t1 = np.asmatrix(np.linspace(0.,max(catalog.Times), groups))        # Generate evenly spaced time values
t1 = t1.T                                                           # transpose into 1 column matrix
r1 = t1 * catalog.D         # multiply to get theoretical squareddistance values
r1 = np.sqrt(r1)            # root to get true distance values

coefficients =  np.polyfit(catalog.Times, catalog.Relative_distances, 2)

# Generate curve to be plotted
x = np.array(np.linspace(0.,max(catalog.Times),groups))       # Generate x values for curve
r1 = r1.T                                                       # Generate y values for curve
r1 = np.array(r1)
y=[]
for value in np.ndenumerate(r1):
    y.append(value[1])
y = np.array(y)
z = np.polyfit(x,y,3)                                   # Generate z polyfit
p = np.poly1d(z)
xp = np.linspace(0,catalog.tlimit, 10)


# Plot map view
point_color = 'red'
mappy=False
if mappy==True:
    geomap = plt.figure()
    ax1 = plt.axes([0.075, 0.01, 0.875, 0.975])
    map = Basemap(llcrnrlon=catalog.minlon ,llcrnrlat=catalog.minlat,urcrnrlon=catalog.maxlon,
        urcrnrlat=catalog.maxlat, epsg=4269, projection='tmerc')
    map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2500,dpi=150, verbose= True, ax=ax1)
    ax1.set_alpha(0.5)
    parallels = np.arange(round(catalog.minlat),round(catalog.maxlat,1),0.2)
    map.drawparallels(parallels,labels=[True, False, False, False],linewidth=0)
    meridians = np.arange(round(catalog.minlon,1),round(catalog.maxlon,1),0.2)
    map.drawmeridians(meridians,labels=[False, False, False, True],linewidth=0)
    ax1.scatter(catalog.Lons, catalog.Lats, color = point_color)
    plt.title('COSO EARTHQUAKE SWARM', fontweight='bold')
    plt.show()

# Plot distances vs time
plt.scatter(catalog.Times, catalog.Relative_distances, color = point_color)
plt.plot(xp,p(xp),'-')
plt.title('COSO EQ Swarm Diffusion')
plt.ylabel('DISTANCE (KM)')
plt.xlabel('TIME (DECIMAL DAY)')
plt.xlim(0.0, 1.0)
plt.ylim(0., 100.)

plt.show()