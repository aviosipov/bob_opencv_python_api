import win32gui
from pywinauto.findwindows    import find_window
from pywinauto.win32functions import SetForegroundWindow
import ImageGrab
import cv2
import helpers
import numpy as np
import paho.mqtt.client as mqtt
import redis
import pickle

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


r = redis.StrictRedis(host='localhost', port=6379, db=0)
client = mqtt.Client()
client.on_connect = on_connect
client.connect("127.0.0.1", 1883, 60)

thing_id = 'bob30'


def get_rect(hwnd):
	rect = win32gui.GetWindowRect(hwnd)
	return rect


def screen_grab():
	box = (x1, y1, x2, y2)
	im = ImageGrab.grab(box)
	return im


def update_thing_shadow(thing_id,data):

	tmp = r.get(thing_id)

	if (tmp is None):
		r.set(thing_id,pickle.dumps(data))
	else:

		tmp = pickle.loads(tmp)
		tmp.update(data)

		r.set(thing_id, pickle.dumps(tmp))




window = find_window(title="bob_robot_sim")
SetForegroundWindow(window)
x1,y1,x2,y2 = get_rect(window)

while (True):

	image = screen_grab()
	img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
	img, thresh, response = helpers.detectTriangles(img)
#	img, response = helpers.detectCircles(img)

	update_thing_shadow(thing_id,response)
	client.publish(thing_id + '/sensors/camera', payload=pickle.dumps(response))

	# Display the resulting frame
	cv2.imshow('result', img)
	cv2.imshow('threshold', thresh)



	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cv2.destroyAllWindows()












