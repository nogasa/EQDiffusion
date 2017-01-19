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
catalog.minyear, catalog.minmonth, catalog.minday = 2016., 9.0, 26.0
catalog.minlat, catalog.minlon = 33.192, -115.876
catalog.maxlat, catalog.maxlon = 33.468, -115.631
catalog.dlimit = 50.

# Pull data
catalog.harvest_USGS('./USGSSaltonSeaCatalog2.xls')
for date in catalog.Decimal_dates:
    catalog.relative_decimal_dates.append(date - min(catalog.Decimal_dates))

# Determine first quake of the swarm
min_time = min(catalog.Decimal_dates)
min_index = catalog.Decimal_dates.index(min_time)

# Determine relative distances between all events and first event
i=0
for event in catalog.Decimal_dates:
    lon1, lat1, lon2, lat2 = map(radians, [catalog.Lons[min_index], catalog.Lats[min_index],
                                           catalog.Lons[i], catalog.Lats[i]])
    km = mf.haversine_distance(lon1,lat1,lon2,lat2)
    catalog.Relative_distances.append(km)
    i=i+1

print catalog.Decimal_dates

# Generate curve for plotting
groups =20.                                           # number of time intervals to construct
dmaxima, tmaxima = catalog.find_maxima(groups)         # finds the max value in each time interval
for value in dmaxima:                                  # square each distance value
    d = value**2
    catalog.r.append(d)
catalog.t = tmaxima                                    # establishes t array from the maxima array
catalog.t = np.asmatrix(catalog.t)                     # convert t array to t matrix
catalog.t = catalog.t.T                                # transpose t matrix into 1 column t matrix
catalog.r = np.asmatrix(catalog.r)                     # convert r array to r matrix
catalog.r = catalog.r.T                                # transpose r matrix into 1 column r matrix
catalog.D,residuals,rank,s = np.linalg.lstsq(catalog.t,catalog.r)           # LEAST SQUARES OPERATION

# Printing routine
print 'r'
print catalog.r
print 't'
print catalog.t
print 'D'
print catalog.D/4/np.pi

# Generate points to be used to plot curve
t1 = np.asmatrix(np.linspace(0.,max(catalog.relative_decimal_dates), groups))        # Generate evenly spaced time values
t1 = t1.T                                                           # transpose into 1 column matrix
r1 = t1 * catalog.D         # multiply to get theoretical squareddistance values
r1 = np.sqrt(r1)            # root to get true distance values


# Generate curve to be plotted
x = np.array(np.linspace(0.,max(catalog.relative_decimal_dates),groups))       # Generate x values for curve
r1 = r1.T                                                       # Generate y values for curve
r1 = np.array(r1)
y=[]
for value in np.ndenumerate(r1):
    y.append(value[1])
y = np.array(y)
z = np.polyfit(x,y,2)                                   # Generate z polyfit
p = np.poly1d(z)
xp = np.linspace(0,catalog.tlimit, 10)

print x
print y

# Plot map view
point_color = 'lightblue'
mappy = False
if mappy == True:
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
    plt.title('SALTON SEA EARTHQUAKE SWARM', fontweight='bold')
    plt.show()

plotty = True
if plotty == True:
    # Plot distances vs time
    plt.scatter(catalog.relative_decimal_dates, catalog.Relative_distances, color = point_color)
    plt.scatter(tmaxima, dmaxima, color='blue')
    plt.scatter(x,y,color='black')
    plt.plot(xp,p(xp),'-', color='black')
    plt.title('SALTON SEA EQ Swarm Diffusion - since 9/26/2016')
    plt.ylabel('DISTANCE (KM)')
    plt.xlabel('TIME (DECIMAL YEARS)')
    plt.xlim(min(catalog.relative_decimal_dates)-0.1,max(catalog.relative_decimal_dates))
    plt.ylim(0., 5.)
    plt.show()