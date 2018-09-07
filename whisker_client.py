#!/usr/bin/python3

import asyncio
import time
from whisker_conn import WhiskerConnector
from concurrent.futures import CancelledError

port = 3233


class WhiskerClient:
	def __init__(self, loop, host, port):
		self.loop = loop
		self.host = host
		self.port = port
		self.main_conn = WhiskerConnector()
		self.imm_conn = None
		self.imm_port = None
		self.imm_code = None
		self.imm_conn_future = asyncio.Future()
		self.imm_reply_future = None
		self.filename = self.get_filename()
	
	def get_filename(self):
		timenow = time.localtime(time.time())
		order = [2,1,0,3,4]
		punctuation = ['-', '-', ' - ', '-', '']
		date = 'Stage 3 R3 '
		for i in range(len(order)):
			date += str(timenow[order[i]])
			date += punctuation[i]
		return(str(date))
	
	@asyncio.coroutine
	def connect(self):
		self.main_conn.add_handler('*', self.handle_main_all)
		self.main_conn.add_handler('ImmPort:', self.handle_Imm)
		self.main_conn.add_handler('Code:', self.handle_Code)
		self.main_conn.add_handler('Event:', self.handle_Event)
		print("Connecting to Whisker Server at {}:{}".format(self.host, self.port))
		yield from self.main_conn.connect(self.loop, 'localhost', self.port)
		yield from self.imm_conn_future

	def handle_main_all(self, m):
		if m is None:
			self.loop.stop()
			print("Server disconnected. Exiting.")
		else:
			print("Main: '" + " ".join(m) + "'")
	
	def handle_reply(self, m):
		pass
		# print(', '.join(m))

	def handle_Imm(self, m):
		self.imm_port = int(m[1])

	def send_message(self, *m):
		# print("Sent: '" + " ".join(m) + "'")
		self.imm_conn.send_message(m)

	@asyncio.coroutine
	def handle_Code(self, m):
		self.imm_code = m[1]
		self.imm_conn = WhiskerConnector()
		self.imm_conn.add_handler('*', self.handle_reply)
		yield from self.imm_conn.connect(self.loop, 'localhost', self.imm_port)
		self.send_message('Link', self.imm_code)
		print("Connecting to immediate channel {}:{} with code {}".format(self.host, self.imm_port, self.imm_code))
		self.imm_conn_future.set_result(True)
#________________________________________________________________________________________________    @asyncio.coroutine
	def handle_Event(self, m):
		message = m[1]

		if message == 'BGTouchDown':
			print('yay')

		# handle event! log it somewhere whatever
		pass
#________________________________________________________________________________________________    
	@asyncio.coroutine
	def setup(self,subject):
		print('Setup for subject: G'+ str(subject))
		if subject == 1:
			houselight = '32'
			traylight = '33'
			food = '34'
			noise = '35'
			traysensor = '0'
			display = '0'
		if subject == 2:
			houselight = '40'
			traylight = '41'
			food = '42'
			noise = '43'
			traysensor = '8'
			display = '1'
		if subject == 3:
			houselight = '48'
			traylight = '49'
			food = '50'
			noise = '51'
			traysensor = '16'
			display = '2'
		if subject == 4:
			houselight = '56'
			traylight = '57'
			food = '58'
			noise = '59'
			traysensor = '24'
			display = '3'
		
		self.send_message('LineClaim', houselight)
		self.send_message('LineClaim', food)
		self.send_message('LineClaim', traylight)
		self.send_message('LineClaim', noise)
		self.send_message('LineClaim', traysensor)
		self.send_message('LineSetState', houselight, 'on')
		self.send_message('LineSetState', traylight, 'off')
		self.send_message('LineSetState', noise, 'off')
		#Display
		self.send_message('DisplayClaim', display)
		self.send_message('DisplayCreateDocument', 'doc')
		self.send_message('DisplayShowDocument', display, 'doc')
		self.send_message('DisplaySetBackgroundColour', 'doc', '0', '0', '0')
		#Timestamps and event co-ordinates
		self.send_message('TimeStamps', 'on')
		self.send_message('DisplayEventCoords', 'on')
		#Touch handlers
		self.send_message('DisplaySetBackgroundEvent', 'doc', 'TouchDown', 'BGTouchDown')
		self.send_message('DisplaySetBackgroundEvent', 'doc', 'TouchUp', 'BGTouchUp')

#________________________________________________________________________________________________

