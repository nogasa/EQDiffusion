from pyproj import Proj, transform
import numpy as np
from pandas import DataFrame

def convertSP2WGS84LL(x,y):
   wgs84_proj = Proj('+proj=longlat +datum=WGS84 +no_defs')
   stateplane_nad83_proj = Proj(init='EPSG:2873',preserve_units=True)
   lat,lon = transform(stateplane_nad27_proj,wgs84_proj,x,y)
   return lat,lon


if __name__ == '__main__':
   well = np.loadtxt(.....)

   lat,lon = convertSP2WGS84LL(well[:,1],well[:,2])
   dep = well[:,2]*.3048

   gm1Out = np.vstack(( lat, lon, dep))

   np.savetxt('/Users/okaven/research/decatur/metadata/GM1_sensorsLocations.wgs84',
                    np.transpose(gm1Out),newline='\n',comments='# ',
                    fmt='%3.8f, %3.8f, %4.6f')

   
