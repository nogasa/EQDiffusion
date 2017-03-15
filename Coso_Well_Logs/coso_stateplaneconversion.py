from pyproj import Proj, transform
import numpy as np
from pandas import DataFrame

def convertSP2WGS84LL(x,y):
   wgs84_proj = Proj('+proj=longlat +datum=WGS84 +no_defs')
   stateplane_nad83_proj = Proj(init='EPSG:2873',preserve_units=True)
   lat,lon = transform(stateplane_nad27_proj,wgs84_proj,x,y)
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
GREATER_FILE_PATH = './3Dwells/tables/''
IDNUM =

inputpath = GREATER_FILE_PATH + LEASE + '/' + NAME + FILE_TYPE
outputpath = GREATER_FILE_PATH + LEASE + '/' + IDNUM + '.txt'


W7319 = Well()
W7319.harvest(inputpath)
for linenum in W7319.Id:
   lat,lon = convertSP2WGS84LL(self.northing[linenum-1], self.easting[linenum-1])
   lat,lon = convertSP2WGS84LL(well[:,1],well[:,2])         # Create lat, lon arrays
   dep = self.elevation[linenum-1]*.3048                                    # Convert feet to meters
   self.lat.append(lat)
   self.lon.append(lon)
   self.z.append(dep)



np.savetxt('./Converted well logs/BLM/027-90217.txt',
                    np.transpose(gm1Out),newline='\n',comments='# ',
                    fmt='%3.8f, %3.8f, %4.6f')

   
