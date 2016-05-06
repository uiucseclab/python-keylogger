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

class screenCapper(threading.Thread):
	outpuDir = ""
	paused = False
	def __init__(self, queue, args=(), kwargs=None):
		global outputDir
		global paused
		self.duration = 60
		paused = False
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.queue = queue
		self.daemon = False
		self.receive_messages = args[0]
		outputDir = args[1]
		
	def isPaused(self):
		global paused
		return paused

	def run(self):
		print(threading.currentThread().getName() + " beginning screen capture")
		global outputDir
		global paused
		lastRun = time.time()
		val = ""
		while True:
			time.sleep(5)
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
			if not paused and (time.time() - lastRun > self.duration or val == "capture"):
				now = datetime.datetime.now()
				lastRun = time.time()
				fileName = (str(now.month) + 
					"_" + str(now.day) + "_" + str(now.year) +
					"_" + str(now.hour) + "_" + str(now.minute) +
					"_" + str(now.second) + "_screen.png")
				outFile = outputDir + fileName
				screenCap.capture(outFile)