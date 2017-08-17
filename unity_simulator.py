import win32gui
from pywinauto.findwindows    import find_window
from pywinauto.win32functions import SetForegroundWindow
import ImageGrab
import cv2
import helpers
import numpy as np
import random

thing_id = 'bob30'
helpers.init()


def get_rect(hwnd):
	rect = win32gui.GetWindowRect(hwnd)
	return rect


def screen_grab():
	box = (x1, y1, x2, y2)
	im = ImageGrab.grab(box)
	return im


window = find_window(title="bob_robot_sim")
SetForegroundWindow(window)
x1,y1,x2,y2 = get_rect(window)


class RandomNoise:

	random_signal_counter = 0

	def __init__(self):
		pass

	def get_signal(self):

		if self.random_signal_counter > 0 :
			self.random_signal_counter -= 1
			return True

		if random.randint(1, 100) < 20:
			self.random_signal_counter = random.randint(1, 8)

		return False

r = RandomNoise()

while True:

	image = screen_grab()
	img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

	# randomly generate noise / blur input

	if r.get_signal():
		img = cv2.GaussianBlur(img, (25, 25), 0)

	# helpers.save_image(img)

	img, thresh, response = helpers.detectTriangles(img)
	helpers.update_thing_shadow(thing_id,response)

	# Display the resulting frame
	cv2.imshow('result', img)
	# cv2.imshow('threshold', thresh)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cv2.destroyAllWindows()

