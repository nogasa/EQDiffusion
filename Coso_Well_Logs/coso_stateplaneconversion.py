from pyproj import Proj, transform
import numpy as np
from pandas import DataFrame
import os, sys

def convertSP2WGS84LL(x,y):
   wgs84_proj = Proj('+proj=longlat +datum=WGS84 +no_defs')
   stateplane_nad83_proj = Proj(init='EPSG:2873',preserve_units=True)
   lat,lon = transform(stateplane_nad83_proj,wgs84_proj,x,y)
   return lat,lon

class Well():
   def __init__(self):
      self.name = 'unnamed'
      self.lease = ' '
      self.Id = []
      self.northing = []
      self.easting = []
      self.elevation = []
      self.temp = []
      self.type = []
      self.lat = []
      self.lon = []
      self.z = []

   def harvest(self, filename):
      '''
      Gathers data for the specified well and compiles them into arrays.

      :arg filename:       the well log file to pull data from
      :type filename:      basestring
      :rtype:              none
      :return:             none
      '''
      well = open(filename)               # open up the data file
      fname = filename.split('/')         # segment filepath string
      fname[3] = self.lease               # gather lease from filepath
      fname[4] = self.name                # gather name from filepath
      self.name = self.name[:-4]          # cut off trailing '.TXT' or '.csv'
      i=1
      for line in well:
         if i>1:                             # Compile data arrays
            Line = line.split(',')
            self.Id.append(Line[0])
            self.northing.append(Line[1])
            self.easting.append(Line[2])
            self.elevation.append(Line[3])
            self.temp.append(Line[4])
            self.type.append(Line[5])
         i=i+1


if __name__ == '__main__':                              # If run as a script...

	# Specify the lease and well number
	LEASE = 'BLM'
	NAME = '73-19'
	FILE_TYPE = '.csv'
	GREATER_FILE_PATH = './3Dwells/tables/'
	#IDNUM = '027-90217'

	inputpath = os.path.join(GREATER_FILE_PATH, LEASE,  NAME + FILE_TYPE)
	#outputpath = GREATER_FILE_PATH + LEASE + '/' + IDNUM + '.txt'


	W7319 = Well()
	W7319.harvest(inputpath)
	i=1
	for linenum in W7319.Id:
	   print W7319.elevation
	   lat,lon = convertSP2WGS84LL(W7319.northing[i-1], W7319.easting[i-1])
	   #lat,lon = convertSP2WGS84LL(well[:,1],well[:,2])         # Create lat, lon arrays
	   #print lat,lon
	   dep = int(W7319.elevation[i-1])*.3048                                    # Convert feet to meters
	   print lat, lon, dep
	   print '------'
	   W7319.lat.append(lat)
	   W7319.lon.append(lon)
	   W7319.z.append(dep)
	   i+=1



	np.savetxt('./Converted well logs/BLM/027-90217.txt',
						np.transpose(gm1Out),newline='\n',comments='# ',
						fmt='%3.8f, %3.8f, %4.6f')

   
