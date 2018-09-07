#!/usr/bin/python3
import numpy as np
import csv

class Session:
	def __init__(self):
		self.subject = 1 #input("Subject: ")
		self.pairs = self.get_pairs()
		self.order = np.random.permutation(np.arange(100))
		self.angles = self.get_angles()
		self.locations = self.get_locations()

	def get_coords(side,length, angle):
		opp = (length/2)*(np.sin((np.radians(90-angle))))
		adj = np.sqrt((length/2)**2 - opp**2)
		if side == 0:
			x0 = 192
		elif side == 1:
			x0 = 576
		else:
			print('Error setting origin')
		y0 = 192
		x1 = int(round(x0 - opp, 0))
		x2 = int(round(x0 + opp, 0))
		y1 = int(round(y0 - adj, 0))
		y2 = int(round(y0 + adj, 0))
		coords = [x1, y1, x2, y2]
		return coords

	def get_angles(self):
		angles = np.array([(np.random.randint(179),np.random.randint(179)) for i in range(100)]).astype("int")
		return angles

	def get_pairs(self):
		reader = csv.reader(open("pairs.csv", "rt"), delimiter=",")
		x = list(reader)
		pairs = np.array([(row[0],row[1]) for row in x]).astype("int")
		return pairs

	def get_locations(self):
		reader = csv.reader(open("pairs.csv", "rt"), delimiter=",")
		x = list(reader)
		scaledLocations = np.array([row[2] for row in x]).astype("float")
		pxLocations = list(map(int,map(lambda x: x*632+68,scaledLocations)))
		return pxLocations


	'''def run():
		#import values
		#pairs = get_pairs()
		#get order
		#order = np.random.permutation(np.arange(100))
		#get angles
		#angles = get_angles()
		#print(order)
		#start experiment
		trial = 1

		#get first 10 coords
		for i in range(10):
			index = order[i]
			coords=[]
			for j in range(2):
				l = pairs[i][j]
				a = angles[i][j]
				coords.append(get_coords(j,l,a))'''

