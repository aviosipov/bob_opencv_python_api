import cv2
import urllib
import numpy as np
import  helpers
import time

stream=urllib.urlopen('http://192.168.1.15:8080/video')
bytes=''


thing_id = 'bob30'
helpers.init()

fps = 0
current_time = 0
start_time = time.time()


while True:

	bytes += stream.read(1024)
	a = bytes.find('\xff\xd8')
	b = bytes.find('\xff\xd9')

	if a != -1 and b != -1:

		diff = time.time() -  start_time

		if diff >= 1:
			print fps
			start_time = time.time()
			fps = 0

		fps += 1

		jpg = bytes[a:b+2]
		bytes = bytes[b+2:]

		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)

		# process data
		img, thresh, response = helpers.detectTriangles(img)
		helpers.update_thing_shadow(thing_id, response)

		# display
		cv2.imshow('result',img)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# When everything done, release the capture
cv2.destroyAllWindows()