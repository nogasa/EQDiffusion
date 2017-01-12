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
    if year%4.==0:
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
        self.minlat = 0.
        self.maxlat = 0.
        self.minlon = 0.
        self.maxlon = 0.
        self.minyear = 0.
        self.minmonth = 0.
        self.minday = 0.
        self.maxyear = 0.
        self.maxmonth = 0.
        self.maxday = 0.
        self.minmag = 0.
        self.maxmag = 0.
        self.mindepth = 0.
        self.maxdepth = 0.

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
        print 'harvest from NCDEC Earthquake Catalog'

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
        print 'harvested from USGS Earthquake catalog'

    def harvest_SCDEC(self,filename, boundaries=False):
        '''
        Harvests data from a downloaded SCDEC text file

        :param filename:    filepath from which to pull data from
        :type filename:     string
        :rtype:             none
        :return:            none
        '''
        file = open(filename)
        for line in file:
            Line = line.split()
            if __name__ == '__main__':
                if boundaries==False:              # If no boundaries are given...gather ALL data
                    year = Line[0]
                    month = Line[1]
                    day = Line[2]
                    decdate = date_to_dec(year, month, day)
                    self.Dates.append(decdate)
                    a = float(Line[3])
                    b = float(Line[4])
                    c = float(Line[5])
                    dec_time = (a / 24.) + (b / (24. * 60.)) + (c / (24. * 60 * 60))
                    self.Times.append(dec_time)
                    self.Lats.append(float(Line[7]))
                    self.Lons.append(float(Line[8]))
                    self.Depths.append(float(Line[9]))
                    self.Mags.append(float(Line[10]))
                if boundaries==True:               # If boundaries ARE given..gather SPECIFIED data
                    year = Line[0]
                    month = Line[1]
                    day = Line[2]
                    if year == self.minyear:
                        if month == self.minmonth:
                            if day == self.minday:
                                decdate = date_to_dec(year, month, day)
                                a = float(Line[3])
                                b = float(Line[4])
                                c = float(Line[5])
                                dec_time = (a / 24.) + (b / (24. * 60.)) + (c / (24. * 60 * 60))
                                if float(Line[7]) >= self.minlat:
                                    if float(Line[7]) <= self.maxlat:
                                        if float(Line[8]) >= self.minlon:
                                            if float(Line[9]) >=self.maxlon:
                                                self.Dates.append(decdate)
                                                self.Times.append(dec_time)
                                                self.Lats.append(float(Line[7]))
                                                self.Lons.append(float(Line[8]))
                                                self.Depths.append(float(Line[9]))
                                                self.Mags.append(float(Line[10]))
        print 'harvested from SCDEC Earthquake catalog'

# Define catalog
catalog = catalog()

# Pull data
#catalog.harvest_NCDEC('./NCDECatalog.txt')
catalog.harvest_SCDEC('./SCDECatalog(81-11).txt')
#catalog.harvest_USGS('./USGSCatalog.xls')

# Randomly select an event as a baseline
count = len(catalog.Decimal_dates)
R = random.randint(1,count)
Rdate = catalog.Decimal_dates[R]

print 'Randomized int: '+ str(R)
print 'EQs in catalog: ' + str(count)

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
print 'distance limit: ' + str(distance) + ' km'
print 'time limit: ' + str(timespan) + ' years'


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
    if key[1]<Rdate + (1./12.):
        month1.append(key)
        month_list.append(month1)
        continue
    if key[1]<Rdate + (2./12.):
        month2.append(key)
        month_list.append(month2)
        continue
    if key[1]<Rdate + (3./12.):
        month3.append(key)
        month_list.append(month3)
        continue
    if key[1]<Rdate + (4./12.):
        month4.append(key)
        month_list.append(month4)
        continue
    if key[1]<Rdate + (5./12.):
        month5.append(key)
        month_list.append(month5)
        continue
    if key[1]<Rdate + (6./12.):
        month6.append(key)
        month_list.append(month6)
        continue
    if key[1]<Rdate + (7./12.):
        month7.append(key)
        month_list.append(month7)
        continue
    if key[1]<Rdate + (8./12.):
        month8.append(key)
        month_list.append(month8)
        continue
    if key[1]<Rdate + (9./12.):
        month9.append(key)
        month_list.append(month9)
        continue
    if key[1]<Rdate + (10./12.):
        month10.append(key)
        month_list.append(month10)
        continue
    if key[1]<Rdate + (11./12.):
        month11.append(key)
        month_list.append(month11)
        continue
    if key[1]<Rdate + (12./12.):
        month12.append(key)
        month_list.append(month12)
        continue

refined_month_list = []
for month in month_list:
    if not month:
        continue
    else:
        refined_month_list.append(month)

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
for key in maxima:
    t.append(float(key[1]))
    timez.append(float(key[1]))
    r.append(float(key[0])**2)

# Convert to numpy matrices and transpose
r = np.asmatrix(r)
t = np.asmatrix(t)
r = r.T
t = t.T


# Perform least squares solution to generate D value

tzero = t-np.tile(Rdate,(len(t),1))
print(tzero.flatten())
print(np.zeros(len(tzero)))
A = np.vstack([tzero.flatten(), np.zeros(len(tzero)).T]).T

D4pi, residuals, rank, s = np.linalg.lstsq(A, r)
print(D4pi)
print 'D value: ' + str(D4pi[0])+'*4pi'

# Use D value and t matrix to generate a 'r' values, which represent the curve
<<<<<<< HEAD
r1 = t * D
r1 = np.sqrt(r1)

# Generate time array to plot r1 against
timez = []
while i <12:
    timez.append(Rdate + (float(i)/12.))

=======
r1 = np.sqrt(t * D4pi[0])

print 'Curve values:'+str(r1)
print 'Curve times:'+str(timez)
>>>>>>> origin/master

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
plt.plot(tzero+Rdate, r1, c='black')



#plt.xlim(Rdate, Rdate+timespan)
#plt.ylim(0.0, distance)
plt.xlabel('Time')
plt.ylabel('Distance')
plt.show()
