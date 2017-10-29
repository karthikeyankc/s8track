import requests
from datetime import datetime
import math
import ephem

# Get current TLE data from NORAD
url = "http://www.celestrak.com/NORAD/elements/stations.txt"
headers = {'Accept': 'text/html', 'User-Agent': 's8track 0.0.1'}
r = requests.get(url, headers=headers)
TLE_data = r.text

# Sat details and Observer data
# TODO Use a GUI
sat_name = "ISS (ZARYA)"
observer_lattitude = "11"
observer_longitude = "76"
observer_date = '2017/10/15'

# TLE data for sat_name
lines = iter(TLE_data.splitlines())

for line in lines:
	if sat_name in line:
		line_1 = line.encode('utf-8')
		line_2 = next(lines).encode('utf-8')
		line_3 = next(lines).encode('utf-8')

''' Realtime position of the satellite/station '''
class Sat:
	def sat_position(self, l1, l2, l3):
		self.sat = ephem.readtle(l1, l2, l3)
		now = datetime.utcnow()
		self.sat.compute(now)
		print '\nCurrent Co-ordinates for %s: %s, %s\n' %(sat_name, math.degrees(self.sat.sublong), math.degrees(self.sat.sublat))
		print 'Elevation: %s meter\n' %self.sat.elevation

	''' Transit estimation '''
	def sat_transit(self, lat, long, date):
		observer = ephem.Observer()
		observer.lat = lat
		observer.long = long
		observer.date = date

		info = observer.next_pass(self.sat)
		#TODO Find sat positions throughout the transit
		print """=====================================\n"""
		print "Rise time = %s" %info[0]
		print "Rise azimuth = %s" %math.degrees(info[1])
		print "Max alttitude time = %s" %info[2]
		print "Max alttitude = %s" %math.degrees(info[3])
		print "Set time = %s" %info[4]
		print "Set azimuth = %s" %math.degrees(info[5])

s = Sat()
print "\ns8 Tracker"
print """====================================="""
s.sat_position(line_1, line_2, line_3)
s.sat_transit(observer_lattitude, observer_longitude, observer_date)