import win32gui
from pywinauto.findwindows    import find_window
from pywinauto.win32functions import SetForegroundWindow
import ImageGrab
import os
import time
import cv2
import helpers
import numpy as np

def getRect(hwnd):
	rect = win32gui.GetWindowRect(hwnd)
	return rect


def screenGrab():
	box = (x1, y1, x2, y2)
	im = ImageGrab.grab(box)
	return im
#	im.save(os.getcwd() + '\\full_snap__' + str(time.time()) +
#			'.png', 'PNG')


window = find_window(title="bob_robot_sim")
SetForegroundWindow(window)

x1,y1,x2,y2 = getRect(window)

while (True):

	image = screenGrab()
	time.sleep(0.03)

	img = np.array(image)  # this is the array obtained from conversion


	img, thresh, response = helpers.detectTriangles(img)

	# Display the resulting frame
	cv2.imshow('frame', img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cv2.destroyAllWindows()












