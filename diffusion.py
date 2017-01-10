import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
import matplotlib.pyplot as plt
import random
import xlrd
'''
Selects a random earthquake and plots other earthquakes' relative distances vs time
'''

def date_to_dec(year, month, day):
    year = float(year)
    month = float(month)
    int_month = int(month)
    day = float(day)
    # account for leap years in February
    if year%4==0:
        feb = 29.
    else:
        feb = 28.
    dayspermonth = [31., feb, 31., 30., 31., 30., 31., 31., 30., 31., 30., 31. ]
    # Determine how many days in the year lead up to the given day
    days_in_months_passed = sum(dayspermonth[:int_month])
    total_days_passed = days_in_months_passed + day
    decimal_year = year + total_days_passed/sum(dayspermonth)
    return decimal_year

def time_to_dec(time):
    Time = time.split(':')
    a = float(Time[0])
    b = float(Time[1])
    c = float(Time[2])
    dec_time = (a/24.)+(b/(24.*60.))+(c/(24.*60*60))
    return dec_time


class catalog():
    def __init__(self):
        self.Dates = []
        self.Times = []
        self.Lats = []
        self.Lons = []
        self.Depths = []
        self.Mags = []
        self.Decimal_dates = []

    def harvest_NCDEC(self,filename):
        '''
        Harvests data from a downloaded NCDEC txt file.

        :param filename:    filepath from which to pull data
        :type filename:     string
        :rtype:             none
        :return:            none
        '''
        file = open(filename)
        for line in file:
            if line_num >= 3:
                Line = line.split()
                date = Line[0]
                time = Line[1]
                lat = Line[2]
                lon = Line[3]
                depth = Line[4]
                mag = Line[5]
                magt = Line[6]
                nst = Line[7]
                gap = Line[8]
                clo = Line[9]
                rms = Line[10]
                src = Line[11]
                self.Dates.append(date)
                self.Times.append(time)
                self.Lats.append(float(lat))
                self.Lons.append(float(lon))
                self.Depths.append(float(depth))
                self.Mags.append(float(mag))
            line_num = line_num + 1
        # Convert dates to decimal dates
        for date in self.Dates:
            Date = date.split('/')
            year = float(Date[0])
            month = float(Date[1])
            day = float(Date[2])
            decimal_date = date_to_dec(year, month, day)
            self.Decimal_dates.append(decimal_date)

    def harvest_USGS(self,filename):
        '''
        Harvests data from a downloaded USGS csv excel file

        :param filename:    filepath from which to pull data from
        :type filename:     string
        :rtype:             none
        :return:            none
        '''
        book = xlrd.open_workbook(filename)
        sheet1 = book.sheet_by_index(0)
        i=1
        while i < sheet1.nrows:
            # Configure cell date to appendable datetime
            datecell = str(sheet1.cell(i,0))
            date = datecell[7:-2]
            self.Dates.append(date)
            # Configure cell lat to appendable lat
            latcell = str(sheet1.cell(i,1))
            lat = latcell[7:]
            self.Lats.append(float(lat))
            # Configure cell lon to appendable lon
            loncell = str(sheet1.cell(i,2))
            lon = loncell[7:]
            self.Lons.append(float(lon))
            # Configure cell depth to appendable depth
            depthcell = str(sheet1.cell(i,3))
            depth = depthcell[7:]
            self.Depths.append(float(depth))
            # Configure cell magnitude to appendable magnitude
            magcell = str(sheet1.cell(i,4))
            mag = magcell[7:]
            self.Mags.append(float(mag))
            i=i+1
        # Convert given datetime into decimal dates / generate self.Times array
        for date in self.Dates:
            Date = date.split('T')
            datetime = Date[0]
            time = Date[1]
            self.Times.append(time)
            Datetime = datetime.split('-')
            year = float(Datetime[0])
            month = float(Datetime[1])
            day = float(Datetime[2])
            decimal_date = date_to_dec(year, month, day)
            decimal_date = decimal_date + time_to_dec(time)
            self.Decimal_dates.append(decimal_date)





# Define catalog
catalog = catalog()

# Pull data
#catalog.harvest_NCDEC('./NCEDCatalog.txt')
catalog.harvest_USGS('./USGSCatalog.xls')

# Randomly select an event as a baseline
count = len(catalog.Decimal_dates)
R = random.randint(1,count)
Rdate = catalog.Decimal_dates[R]

# Calculate the great circle distance between randomly selected point and iteration point
Relative_Distances = []
i=0
for date in catalog.Dates:
    lon1, lat1, lon2, lat2 = map(radians, [catalog.Lons[R], catalog.Lats[R], catalog.Lons[i], catalog.Lats[i]])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    Relative_Distances.append(km)
    i=i+1

Rdistance = Relative_Distances[R]

# Combine dates and distances together into single array
Keys = []
i=0
for value in Relative_Distances:
    Keys.append([Relative_Distances[i], catalog.Decimal_dates[i], catalog.Depths[i], catalog.Mags[i]])
    i=i+1

# Define time span (years) and distance (km)
distance = 20.
timespan = 1.0

# Get rid of any events that happened before random selection
Keys1 = []
for key in Keys:
    if key[1]>Rdate:
        Keys1.append(key)
# Get rid of any events that happened ___ years after random selection
Keys2 = []
for key in Keys1:
    if key[1]<Rdate+timespan:
        Keys2.append(key)
# Get rid of any events that happened ___ km away from the random selection.
Keys3 = []
for key in Keys2:
    if key[0]<distance:
        Keys3.append(key)

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
print R
print Relative_Distances

#plt.xlim(Rdate, Rdate+timespan)
#plt.ylim(0.0, distance)
plt.xlabel('Time')
plt.ylabel('Distance')
plt.show()