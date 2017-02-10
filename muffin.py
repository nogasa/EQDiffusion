import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
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
import random
import xlrd

'''
Module for analyzing earthquake selfs.
'''


def date_to_dec(year, month, day):
    year = float(year)
    month = float(month)
    int_month = int(month)
    day = float(day)
    # account for leap years in February
    if year % 4. == 0:
        feb = 29.
    else:
        feb = 28.
    dayspermonth = [31., feb, 31., 30., 31., 30., 31., 31., 30., 31., 30., 31.]
    # Determine how many days in the year lead up to the given day
    days_in_months_passed = sum(dayspermonth[:int_month])
    total_days_passed = days_in_months_passed + day
    decimal_year = year + total_days_passed / sum(dayspermonth)
    return decimal_year


def time_to_dec(time):
    Time = time.split(':')
    a = float(Time[0])
    b = float(Time[1])
    c = float(Time[2])
    dec_time = (a / 24.) + (b / (24. * 60.)) + (c / (24. * 60 * 60))
    return dec_time


def haversine_distance(lon1, lat1, lon2, lat2):
    '''
    Calculates the great circle distance between two points

    :param lon1:    longitude of point 1
    :param lat1:    latitude of point 1
    :param lon2:    longitude of point 2
    :param lat2:    latitude of point 2
    :type lon1:     float
    :type lat1:     float
    :type lon2:     float
    :type lat2:     float
    :rtype:         float
    :return:        distance in km
    '''
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


class catalog():
    def __init__(self):
        self.Dates = []
        self.Times = []
        self.Lats = []
        self.Lons = []
        self.Depths = []
        self.Mags = []
        self.Mo = []
        self.Decimal_dates = []
        self.relative_decimal_dates = []
        self.E0_time = 0.                       # The first event's datetime of occurence
        self.E0_index = 0                       # The first event's position in the self.Decimal_dates array
        self.minlat = 0.
        self.maxlat = 0.
        self.minlon = 0.
        self.maxlon = 0.
        self.londist = 0.
        self.latdist = 0.
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
        self.random = 0
        self.rand_date = 0.
        self.rand_dist = 0.
        self.Relative_distances = []
        self.dlimit = 0.
        self.tlimit = 0.
        self.t = []
        self.D = []
        self.r = []
        self.D_err = []
        self.summer= False

    def harvest_xyz(self,filename):
        '''
        Harvests data from the forandy file in the data file.

        :param filename:    filepath from which to pull data from
        :type filename:     basestring
        :rtype:             none
        :return:            none
        '''
        file = open(filename)
        for line in file:
            Line = line.split()
            year = Line[0]
            month = Line[1]
            day = Line[2]
            hour = Line[3]
            minute = Line[4]
            second = Line[5]
            mw = Line[6]
            lat = Line[7]
            lon = Line[8]
            depth = Line[9]
            normdist = Line[10]
            reftime = Line[11]
            Decimaldate = (date_to_dec(year, month, day))
            timestring = (str(hour)+':'+str(minute)+':'+str(second))
            time = (time_to_dec(timestring))
            self.Times.append(time)
            self.Decimal_dates.append(Decimaldate + time/365.)
            self.Lats.append(float(lat))
            self.Lons.append(float(lon))
            self.Depths.append(float(depth))
            self.Mags.append(float(mw))
            exp = 1.5 * (float(mw) + 10.7)
            self.Mo.append(10.0**exp)

    def harvest_NCDEC(self, filename):
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

    def harvest_USGS(self, filename):
        '''
        Harvests data from a downloaded USGS csv excel file

        :param filename:    filepath from which to pull data from
        :type filename:     string
        :rtype:             none
        :return:            none
        '''
        book = xlrd.open_workbook(filename)
        sheet1 = book.sheet_by_index(0)
        i = 1
        while i < sheet1.nrows:
            # Configure cell date to appendable datetime
            datecell = str(sheet1.cell(i, 0))
            date = datecell[7:-2]
            self.Dates.append(date)
            # Configure cell lat to appendable lat
            latcell = str(sheet1.cell(i, 1))
            lat = latcell[7:]
            self.Lats.append(float(lat))
            # Configure cell lon to appendable lon
            loncell = str(sheet1.cell(i, 2))
            lon = loncell[7:]
            self.Lons.append(float(lon))
            # Configure cell depth to appendable depth
            depthcell = str(sheet1.cell(i, 3))
            depth = depthcell[7:]
            self.Depths.append(float(depth))
            # Configure cell magnitude to appendable magnitude
            magcell = str(sheet1.cell(i, 4))
            mag = magcell[7:]
            self.Mags.append(float(mag))
            i = i + 1
        # Convert given datetime into decimal dates / generate self.Times array
        for date in self.Dates:
            Date = date.split('T')
            datetime = Date[0]
            time = Date[1]
            time = time[:-2]
            time = time_to_dec(time)
            self.Times.append(time)
            Datetime = datetime.split('-')
            year = float(Datetime[0])
            month = float(Datetime[1])
            day = float(Datetime[2])
            decimal_date = date_to_dec(year, month, day)
            decimal_date = decimal_date + time
            self.Decimal_dates.append(decimal_date)
        print 'harvested from USGS Earthquake self'

    def harvest_SCDEC(self, filename, boundaries=False):
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
            if boundaries == False:  # If no boundaries are given...gather ALL data
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
            if boundaries == True:  # If boundaries ARE given..gather SPECIFIED data
                year = float(Line[0])
                month = float(Line[1])
                day = float(Line[2])
                if year == self.minyear:
                    if month == self.minmonth:
                        if day == self.minday:
                            if float(Line[7]) >= self.minlat:
                                if float(Line[7]) <= self.maxlat:
                                    if float(Line[8]) >= self.minlon:
                                        if float(Line[8]) <= self.maxlon:
                                            decdate = date_to_dec(year, month, day)
                                            a = float(Line[3])
                                            b = float(Line[4])
                                            c = float(Line[5])
                                            dec_time = (a / 24.) + (b / (24. * 60.)) + (c / (24. * 60 * 60))
                                            self.Decimal_dates.append(decdate)
                                            self.Times.append(dec_time)
                                            self.Lats.append(float(Line[7]))
                                            self.Lons.append(float(Line[8]))
                                            self.Depths.append(float(Line[9]))
                                            self.Mags.append(float(Line[10]))
        print 'harvested from SCDEC Earthquake self'

    def process(self):
        '''
        Process data and define necessary class variables.

        :rtype:         none
        :return:        none
        '''
        # Generate relative decimal dates array
        for date in self.Decimal_dates:
            self.relative_decimal_dates.append(date - min(self.Decimal_dates))
        # Generate first earthquake index
        self.E0_time = min(self.Decimal_dates)
        self.E0_index = self.Decimal_dates.index(self.E0_time)
        # Generate relative distances array
        i = 0
        for event in self.Decimal_dates:
            lon1, lat1, lon2, lat2 = map(radians, [self.Lons[self.E0_index], self.Lats[self.E0_index],
                                                   self.Lons[i], self.Lats[i]])
            km = haversine_distance(lon1, lat1, lon2, lat2)
            self.Relative_distances.append(km)
            i = i + 1
        self.minlat = min(self.Lats)
        self.maxlat = max(self.Lats)
        self.minlon = min(self.Lons)
        self.maxlon = max(self.Lons)
        self.londist = self.maxlon - self.minlon
        self.latdist = self.maxlat - self.minlat

    def glean(self, min_time, max_time):
        '''
        Crops out a select portion of the data set and corresponding arrays constructed in
        self.harvest and self.process, based on a minimum and maximum time value.

        :param min_time:        the lower time boundary
        :param max_time:        the upper time boundary
        :type min_time:         float
        :type max_time:         float
        :rtype:                 none
        :return:                none
        '''
        min_time = float(min_time)
        max_time = float(max_time)
        # iterate through dates relative dates array, find values after min time and before max time
        temp_arrayA = []
        for date in self.relative_decimal_dates:
            if date >= min_time:
                if date <= max_time:
                    temp_arrayA.append(date)
        temp_arrayAA = []
        i=0
        for date in temp_arrayA:
            temp_arrayAA.append(date - temp_arrayA[0])
            i=i+1
        # find indices in original list that mark boundary events
        lower_boundary = temp_arrayA[0]
        upper_boundary = temp_arrayA[-1]
        lower_index = self.relative_decimal_dates.index(lower_boundary)
        upper_index = self.relative_decimal_dates.index(upper_boundary)+1
        # Redefine class arrays and variables
        self.relative_decimal_dates = temp_arrayAA
        self.Lats = self.Lats[lower_index:upper_index]
        self.Lons = self.Lons[lower_index:upper_index]
        self.Mags = self.Mags[lower_index:upper_index]
        self.E0_index = self.relative_decimal_dates.index(min(self.relative_decimal_dates))
        temp_arrayB = []
        i=0
        for event in self.relative_decimal_dates:
            lon1, lat1, lon2, lat2 = map(radians, [self.Lons[self.E0_index], self.Lats[self.E0_index],
                                                   self.Lons[i], self.Lats[i]])
            km = haversine_distance(lon1, lat1, lon2, lat2)
            temp_arrayB.append(km)
            i = i + 1
        self.Relative_distances = temp_arrayB
        self.minlat = min(self.Lats)
        self.maxlat = max(self.Lats)
        self.minlon = min(self.Lons)
        self.maxlon = max(self.Lons)
        self.londist = self.maxlon - self.minlon
        self.latdist = self.maxlat - self.minlat



        # redefine them as select portions of themselves


    def randomquake(self):
        '''
        Determines a random integer between 1 and the length of self.Decimal_dates

        :rtype:     integer
        :return:    the random integer
        '''
        count = len(self.Decimal_dates)
        R = random.randint(1, count)
        self.rand_date = self.Decimal_dates[R]
        self.random = R
        print 'Randomized int: ' + str(R)
        print 'EQs pulled from self: ' + str(count)
        return R

    def find_maxima(self, groups):
        '''
        Find maxima for each grouping.

        :param groups:      number of groupings
        :type groups:       float
        :rtype:             array
        :return:            array containing maxima distances and times
        '''
        self.tlimit = max(self.relative_decimal_dates) - min(self.relative_decimal_dates)
        interval = self.tlimit/float(groups)
        dmaxima = []
        tmaxima = []
        i=1
        while i<=groups:
            airlock=[]
            for value in self.relative_decimal_dates:        # Organize dates into airlocks, time representing intervals
                if value<((interval*i)):
                    if value>(interval*(i-1)):
                        airlock.append(value)
            hull = []
            if len(airlock)>=1:                     # If an airlock is constructed...
                for date in airlock:                    # Iterate through dates in the interval
                    index = self.relative_decimal_dates.index(date)      # Find the corresponding distances for the dates
                    hull.append(self.Relative_distances[index])
                maxi = max(hull)
                index2 = self.Relative_distances.index(maxi)
                dmaxima.append(maxi)
                tmaxima.append(self.relative_decimal_dates[index2])
            i = i + 1
        return dmaxima, tmaxima

    def r_matrix(self):
        '''
        Generates the r matrix corresponding to the t-matrix from self.find_maxima

        :rtype:     numpy matrix
        :return:    matrix containing distance values
        '''
        for time in self.t:
            index = self.Decimal_dates.index(time)
            self.r.append((self.Relative_distances[index])**2)

    def summer_squares(self, num_squares):
        '''
        Divides field into a mesh of squares, and sums the Mag of all events within each square.

        :param num_squares      the number of squares/intervals to create on each axis
        :type num_squares       int or float
        :rtype:                 arrays
        :return:                arrays to be plotted
        '''
        # Establish endpoints of each axis
        maxtime = max(self.relative_decimal_dates)
        maxdist = max(self.Relative_distances)
        # Construct arrays containing the intervals for the squares
        time_list = np.linspace(0., maxtime, num_squares)
        dist_list = np.linspace(0., maxdist, num_squares)
        # Compile relative distances and relative times into single, (x,y)-array
        events = []
        i=0
        for value in self.relative_decimal_dates:
            x,y,z = value, self.Relative_distances[i], self.Mags[i]
            events.append([x,y,z])
            i=i+1
        # Establish lists to hold events before they are summed, for each square
        sumsquares=[]
        X=[]
        Y=[]
        Z=[]
        i=0
        for time_iteration in time_list:                         # iterate through columns
            j=0
            for dist_iteration in dist_list:                      # iterate through each row in each column
                TBS=[]
                for event in events:                             # now check all events...
                    if (event[0]>=time_list[i]) & (event[0]<time_list[i+1]):
                        if (event[1]>=dist_list[j]) & (event[1]<dist_list[j+1]):
                            TBS.append([event[2]])
                squaresum = 0.
                for value in TBS:
                    squaresum = squaresum + value[0]
                xx = time_iteration + ((time_list[i+1] - time_iteration)/2.)
                yy = dist_iteration + ((dist_list[j+1] - dist_iteration)/2.)
                X.append(xx)
                Y.append(yy)
                Z.append(squaresum)
                j=j+1
                if j == num_squares-1:
                    break
            i=i+1
            if i == num_squares-1:
                break
            self.summer = True
        return X,Y,Z




    def cartographer(self):
        '''
        Plots events on a basemap. 
        
        :rtype:     none
        :return:    none       
        '''
        geomap = plt.figure(figsize=(9, 9))
        ax1 = plt.axes([0.075, 0.05, 0.875, 0.9])
        map = Basemap(llcrnrlon=self.minlon - self.londist, llcrnrlat=self.minlat - self.latdist,
                      urcrnrlon=self.maxlon + self.londist,
                      urcrnrlat=self.maxlat + self.latdist, epsg=4269, projection='tmerc')
        map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2500, dpi=150, verbose=True, ax=ax1)
        ax1.set_alpha(0.5)
        parallels = np.arange(round(self.minlat-self.latdist,4), round(self.maxlat+self.latdist, 4), 0.01)
        map.drawparallels(parallels, labels=[True, False, False, False], linewidth=0)
        meridians = np.arange(round(self.minlon-self.londist, 4), round(self.maxlon+self.londist, 4), 0.01)
        map.drawmeridians(meridians, labels=[False, False, False, True], linewidth=0)
        ax1.scatter(self.Lons, self.Lats, color = 'lightblue', zorder=11)
        ax1.scatter(self.Lons[self.E0_index], self.Lats[self.E0_index], color = 'red', zorder = 15)
        plt.title('SOCAL EARTHQUAKE SWARM', fontweight='bold')
        # Plot patch representing sampling area
        x1, y1 = map(self.minlon, self.maxlat)
        x2, y2 = map(self.minlon, self.minlat)
        x3, y3 = map(self.maxlon, self.minlat)
        x4, y4 = map(self.maxlon, self.maxlat)
        poly = Polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], alpha=0.2, facecolor='white', edgecolor='black',
                       zorder=10)
        plt.gca().add_patch(poly)
        # Plot text describing patch size
        lon1, lat1, lon2, lat2 = radians(self.minlon), radians(self.minlat), radians(self.minlon), radians(self.maxlat)
        height = haversine_distance(lon1, lat1, lon2, lat2)
        lon1, lat1, lon2, lat2 = radians(self.minlon), radians(self.minlat), radians(self.maxlon), radians(self.minlat)
        width = haversine_distance(lon1, lat1, lon2, lat2)
        plt.text(self.minlon+(self.londist/2.), self.minlat, str(round(width,2))+' km', fontweight='bold')
        plt.text(self.minlon, self.minlat+(self.latdist/2.), str(round(height,2))+' km', fontweight='bold',rotation = 90)

        plt.show()
    
