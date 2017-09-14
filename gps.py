#!/usr/bin/python
from termcolor import colored
import serial
import re


class GPS(object):
	"""docstring for GPS"""
	def __init__(self):
		self.latitude =0.0
		self.longitude =0.0
		self.altitude =0.0
		#self.time=0

	def parse(self,nmea):
		patron = re.compile(r'[$]GPGGA.*')
		gpgga = patron.match(nmea)
		patron = re.compile(r'[$]GPRMC.*')
		gprmc = patron.match(nmea)

		if gpgga != None:
			#time
			data = gpgga.group().split(",")
			time = float(data[1])
			hour = int(time/10000)
			minute = int((time % 10000) / 100)
			second = int((time % 100))
			print data[1] , hour , minute ,second
			#Latitude
			degree = int(data[2][:2])* 10000000
			minutes = int(50*int(data[2][2:4]+data[2][5:])/3)
			self.latitude = degree/100000 + minutes*0.000006 
			latitudeDegrees= (self.latitude-100*int(self.latitude/100))/60.0 + int(self.latitude/100)
			if data[3] == 'S' :
				latitudeDegrees= latitudeDegrees*-1
			
			#Longitude
			degree = int(data[4][:3])*10000000
			minutes = int(50* int(data[4][3:4]+data[4][6:])/3)
			self.longitude = degree/100000 + minutes*0.000006 
			longitudeDegrees=(self.longitude-100*int(self.longitude/100))/60.0 + int(self.longitude/100)
			if data[5] == 'W' :
				longitudeDegrees= longitudeDegrees*-1
			print colored(data,'red') ,degree, minutes, latitudeDegrees, longitudeDegrees

		if gprmc != None:
			data = gprmc.group().split(",")

			print colored(gprmc.group(),'blue')


x = GPS()
f= open('example.txt','r')
for line in f:
	x.parse(line) 		


