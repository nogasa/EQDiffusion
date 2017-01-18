import numpy as np
import scipy as sp
from math import radians, cos, sin, asin, sqrt
from datetime import datetime as dt
import time
import matplotlib.pyplot as plt
import random
import xlrd

'''
Module for analyzing earthquake catalogs.
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
        self.Decimal_dates = []
        self.relative_decimal_dates = []
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
        self.random = 0
        self.rand_date = 0.
        self.rand_dist = 0.
        self.Relative_distances = []
        self.dlimit = 0.
        self.tlimit = 0.
        self.t = []
        self.D = []
        self.r = []

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
        print 'harvested from USGS Earthquake catalog'

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
        print 'harvested from SCDEC Earthquake catalog'

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
        print 'EQs pulled from catalog: ' + str(count)
        return R

    def cull(self, d_limit, t_limit):
        '''
        Cull quakes that do not fall within the given timespan or distance of the random quake.

        :param d_limit:     the distance limit (km)
        :param t_limit:     the timespan (years)
        :type d_limit:      float
        :type t_limit:      float
        :rtype:             array
        :return:            returns the culled list
        '''

    def find_maxima(self, groups):
        '''
        Find maxima for each grouping.

        :param groups:      number of groupings
        :type groups:       float
        :rtype:             array
        :return:            array containing maxima
        '''
        self.tlimit = max(self.Decimal_dates) - min(self.Decimal_dates)
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
                    index = self.relative_decimal_dates.index(date)               # Find the corresponding distances for the dates
                    hull.append(self.Relative_distances[index])
                maxi = max(hull)
                index2 = self.Relative_distances.index(maxi)
                dmaxima.append(maxi)
                tmaxima.append(self.relative_decimal_dates[index2])
            i = i + 1
        return dmaxima, tmaxima

    def r_matrix(self):
        '''
        Generates the r matrix corresponding to the t-matrix from catalog.find_maxima

        :rtype:     numpy matrix
        :return:    matrix containing distance values
        '''
        for time in self.t:
            index = self.Decimal_dates.index(time)
            self.r.append((self.Relative_distances[index])**2)

