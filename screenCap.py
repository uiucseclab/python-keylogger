from PIL import ImageGrab
import time

def capture(output):
	screen = ImageGrab.grab()
	screen.save(output,'png')