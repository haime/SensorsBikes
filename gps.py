#!/usr/bin/python
from termcolor import colored
import serial
import re
import time


class GPS(object):
	"""docstring for GPS"""
	def __init__(self):
		self.latitude =0.0
		self.latitudeDegrees =0.0
		self.longitude =0.0
		self.longitudeDegrees =0.0
		self.altitude =0.0
		self.date = 0.0
		self.satellites=0
		self.fixquality=0
		self.HDOP=0.0
		self.geoidHeight=0.0
		self.speed = 0.0
		self.angle = 0.0

	def parse(self,nmea):
		patron = re.compile(r'[$]GPGGA.*')
		gpgga = patron.match(nmea)
		patron = re.compile(r'[$]GPRMC.*')
		gprmc = patron.match(nmea)

		if gpgga != None:
			###########time
			data = gpgga.group().split(",")
			d= True
			for x in data:
				if x == '' and x!=data[13]:
					d = False
					print "No data received"
			if d:
				time_ = float(data[1])
				hour = int(time_/10000) - 5
				minute = int((time_ % 10000) / 100)
				second = int((time_ % 100))
				
				###########Latitude
				degree = int(data[2][:2])* 10000000
				minutes = int(50*int(data[2][2:4]+data[2][5:])/3)
				self.latitude = degree/100000 + minutes*0.000006 
				self.latitudeDegrees= (self.latitude-100*int(self.latitude/100))/60.0 + int(self.latitude/100)
				if data[3] == 'S' :
					self.latitudeDegrees= latitudeDegrees*-1
				
				###########Longitude
				degree = int(data[4][:3])*10000000
				minutes = int(50* int(data[4][3:5]+data[4][6:])/3)
				self.longitude = degree/100000 + minutes*0.000006 
				self.longitudeDegrees=(self.longitude-100*int(self.longitude/100))/60.0 + int(self.longitude/100)
				if data[5] == 'W' :
					self.longitudeDegrees= self.longitudeDegrees*-1
	
				self.fixquality = int(data[6])
				self.satellites = int(data[7])
				self.HDOP = float(data[8])
				self.altitude = float(data[9])
				self.geoidHeight = float(data[11])  
	
	
				#print colored("Latitude: "+str(self.latitudeDegrees)+" Longitude: "+str(self.longitudeDegrees)+" Altitude: " + str(self.altitude ),'red') ,hour,minute,second

		if gprmc != None:
			data = gprmc.group().split(",")
			d= True
			for x in data:
				if x == '' and x!=data[10] and x!=data[11]:
					d = False
					print "No data received"
			if d:

				##########time
				time_ = float(data[1])
				hour = int(time_/10000) - 5
				minute = int((time_ % 10000) / 100)
				second = int((time_ % 100))

				###########Latitude
				degree = int(data[3][:2])* 10000000
				minutes = int(50*int(data[3][2:4]+data[3][5:])/3)
				self.latitude = degree/100000 + minutes*0.000006 
				self.latitudeDegrees= (self.latitude-100*int(self.latitude/100))/60.0 + int(self.latitude/100)
				if data[4] == 'S' :
					self.latitudeDegrees= latitudeDegrees*-1

				###########Longitude
				degree = int(data[5][:3])*10000000
				minutes = int(50* int(data[5][3:5]+data[5][6:])/3)
				self.longitude = degree/100000 + minutes*0.000006 
				self.longitudeDegrees=(self.longitude-100*int(self.longitude/100))/60.0 + int(self.longitude/100)
				if data[6] == 'W' :
					self.longitudeDegrees= self.longitudeDegrees*-1
			
				self.speed= float(data[7])
				self.angle= float(data[8])

				############Date
				fulldate = float(data[9])
				day = int(fulldate / 10000)
				month = int((fulldate % 10000) / 100)
				year = int(fulldate % 100)+2000
				t= (year, month, day, hour, minute,second,1,48,0)
				self.date = time.mktime(t)
				#print colored("Latitude: "+str(self.latitudeDegrees)+" Longitude: "+str(self.longitudeDegrees)+" Altitude: " + str(self.altitude )+" "+time.asctime(time.localtime(self.date)),'blue')


x = GPS()
f= open('example.txt','r')
for line in f:
	x.parse(line)
	print "Latitude: "+str(x.latitudeDegrees)+" Longitude: "+str(x.longitudeDegrees)+" Altitude: " + str(x.altitude )
	print time.asctime(time.localtime(x.date))


