import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
import matplotlib.pyplot as plt
import random
import xlrd

import muffin as mf
'''
Selects a random earthquake and plots other earthquakes' relative distances vs time
'''

# Define catalog
catalog = mf.catalog()
catalog.minyear, catalog.minmonth, catalog.minday = 1992., 8.0, 1.0
catalog.minlat, catalog.minlon = 33.0, -119.
catalog.maxlat, catalog.maxlon = 36.4, -116.


# Pull data
#catalog.harvest_NCDEC('./NCEDCatalog.txt')
catalog.harvest_SCDEC('./SCEDCatalog(81-11).txt', boundaries=True)
#catalog.harvest_USGS('./USGSCatalog.xls')

# Randomly select an event as a baseline
R = catalog.randomquake()

# Calculate the great circle distance between randomly selected point and iteration point
i=0
for date in catalog.Decimal_dates:
    lon1, lat1, lon2, lat2 = map(radians, [catalog.Lons[R], catalog.Lats[R], catalog.Lons[i], catalog.Lats[i]])
    km = mf.haversine_distance(lon1,lat1,lon2,lat2)
    catalog.Relative_distances.append(km)
    i=i+1

# Name the random point's relative distance
catalog.rand_dist = catalog.Relative_distances[R]

# Combine dates and distances together into single array
Keys = []
i=0
for value in catalog.Relative_distances:
    Keys.append([catalog.Relative_distances[i], catalog.Decimal_dates[i], catalog.Depths[i], catalog.Mags[i]])
    i=i+1

# Define time span (years) and distance (km)
distance = 20.
timespan = 1.0
print 'distance limit: ' + str(distance) + ' km'
print 'time limit: ' + str(timespan) + ' years'


'''
Current problem is that we are pulling already specified quakes from SCEDC, while
the script is still slicing after the fact. Thus, it is culling all the data since it
has two seperate culling routines.

Mode 1: Random quake
generate a random point and analyze points relative to that point.

Mode 2: Swarm
pull in a swarm and observe from the first quake.


'''



# Get rid of any events that happened before random selection
Keys1 = []
for key in Keys:
    if key[1]>catalog.rand_date:
        Keys1.append(key)
# Get rid of any events that happened ___ years after random selection
Keys2 = []
for key in Keys1:
    if key[1]<catalog.rand_date+timespan:
        Keys2.append(key)
# Get rid of any events that happened ___ km away from the random selection.
Keys3 = []
for key in Keys2:
    if key[0]<distance:
        Keys3.append(key)

print Keys3
# Select maximum from each group
month1=[]
month2=[]
month3=[]
month4=[]
month5=[]
month6=[]
month7=[]
month8=[]
month9=[]
month10=[]
month11=[]
month12=[]
month_list = []

i=0
for key in Keys3:
    if key[1]<catalog.rand_date + (1./12.):
        month1.append(key)
        month_list.append(month1)
        continue
    if key[1]<catalog.rand_date + (2./12.):
        month2.append(key)
        month_list.append(month2)
        continue
    if key[1]<catalog.rand_date + (3./12.):
        month3.append(key)
        month_list.append(month3)
        continue
    if key[1]<catalog.rand_date + (4./12.):
        month4.append(key)
        month_list.append(month4)
        continue
    if key[1]<catalog.rand_date + (5./12.):
        month5.append(key)
        month_list.append(month5)
        continue
    if key[1]<catalog.rand_date + (6./12.):
        month6.append(key)
        month_list.append(month6)
        continue
    if key[1]<catalog.rand_date + (7./12.):
        month7.append(key)
        month_list.append(month7)
        continue
    if key[1]<catalog.rand_date + (8./12.):
        month8.append(key)
        month_list.append(month8)
        continue
    if key[1]<catalog.rand_date + (9./12.):
        month9.append(key)
        month_list.append(month9)
        continue
    if key[1]<catalog.rand_date + (10./12.):
        month10.append(key)
        month_list.append(month10)
        continue
    if key[1]<catalog.rand_date + (11./12.):
        month11.append(key)
        month_list.append(month11)
        continue
    if key[1]<catalog.rand_date + (12./12.):
        month12.append(key)
        month_list.append(month12)
        continue
print month_list
refined_month_list = []
for month in month_list:
    if not month:
        continue
    else:
        refined_month_list.append(month)
print refined_month_list
maxima = []
for month in refined_month_list:
    distz = []
    for key in month:
        distz.append(key[0])
    maximum = max(distz)
    index = distz.index(maximum)
    maxima.append(month[index])

# Seperate maxima into two arrays, containing distance and time values. Prep for lstsq solution.
timez = []
t = []
r = []
print maxima
for key in maxima:
    t.append(float(key[1]))
    timez.append(float(key[1]))
    r.append(float(key[0])**2)

# Convert to numpy matrices and transpose
r = np.asmatrix(r)
t = np.asmatrix(t)
r = r.T
t = t.T
print 't'
print t
# Perform least squares solution to generate D value


tdiff = np.tile(catalog.rand_date,(len(t),1))
print 'tdiff'
print tdiff
tzero = t-tdiff
print 'Tzero:'
print tzero
print (tzero.flatten())
print(np.zeros(len(tzero)))
A = np.vstack([tzero.flatten(), np.zeros(len(tzero)).T]).T

D4pi, residuals, rank, s = np.linalg.lstsq(A, r)
print(D4pi)
print 'D value: ' + str(D4pi[0])+'*4pi'

# Use D value and t matrix to generate a 'r' values, which represent the curve

r1 = t * D
r1 = np.sqrt(r1)

# Generate time array to plot r1 against
timez = []
while i <12:
    timez.append(catalog.rand_date + (float(i)/12.))


r1 = np.sqrt(t * D4pi[0])

print 'Curve values:'+str(r1)
print 'Curve times:'+str(timez)


# Plot data points
for key in Keys3:
    if key[2]>7.5:
        plt.scatter(key[1], key[0], c='red', s=40)
    elif key[2]>6.0:
        plt.scatter(key[1], key[0], c='orange', s=40)
    elif key[2]>4.0:
        plt.scatter(key[1], key[0], c='gold', s=40)
    elif key[2]>2.0:
        plt.scatter(key[1], key[0], c='green', s=40)
    elif key[2]>1.0:
        plt.scatter(key[1], key[0], c='blue', s=40)
    else:
        plt.scatter(key[1], key[0], c='purple', s=40)
print 'number of events used: ' + str(len(Keys3))

# Plot calculated curve points
r1 = np.asarray(r1)
plt.plot(tzero+catalog.rand_date, r1, c='black')



#plt.xlim(catalog.rand_date, catalog.rand_date+timespan)
#plt.ylim(0.0, distance)
plt.xlabel('Time')
plt.ylabel('Distance')
plt.show()
