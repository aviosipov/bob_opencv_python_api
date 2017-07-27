from __future__ import division
import numpy as np
import cv2
import redis
import pickle
import paho.mqtt.client as mqtt
import heapq
import time

current_milli_time = lambda: int(round(time.time() * 1000))

r = redis.StrictRedis(host='localhost', port=6379, db=0)
client = mqtt.Client()
min_area = 150

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))


def init():
	client.on_connect = on_connect
	client.connect("127.0.0.1", 1883, 60)


def update_thing_shadow(thing_id,data):

	tmp = r.get(thing_id)

	if tmp is None:
		r.set(thing_id,pickle.dumps(data))
	else:
		tmp = pickle.loads(tmp)
		tmp.update(data)
		r.set(thing_id, pickle.dumps(tmp))

	client.publish(thing_id + '/sensors/camera', payload=pickle.dumps(data))


def save_image(image, prefix = 'cap_' , folder = 'capture'):
	cv2.imwrite( folder + '/' + prefix + str(current_milli_time()) + '.jpg', image)



def rotate_bound(image, angle):
	# grab the dimensions of the image and then determine the
	# center
	(h, w) = image.shape[:2]
	(cX, cY) = (w // 2, h // 2)

	# grab the rotation matrix (applying the negative of the
	# angle to rotate clockwise), then grab the sine and cosine
	# (i.e., the rotation components of the matrix)
	M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
	cos = np.abs(M[0, 0])
	sin = np.abs(M[0, 1])

	# compute the new bounding dimensions of the image
	nW = int((h * sin) + (w * cos))
	nH = int((h * cos) + (w * sin))

	# adjust the rotation matrix to take into account translation
	M[0, 2] += (nW / 2) - cX
	M[1, 2] += (nH / 2) - cY

	# perform the actual rotation and return the image
	return cv2.warpAffine(image, M, (nW, nH))


def rotate(image, angle, center = None, scale = 1.0):
	(h, w) = image.shape[:2]

	if center is None:
		center = (w / 2, h / 2)

	# Perform the rotation
	M = cv2.getRotationMatrix2D(center, angle, scale)
	rotated = cv2.warpAffine(image, M, (w, h))

	return rotated


def detectCircles(img):

	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
	img = cv2.medianBlur(img, 5)
	cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

	circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 1, 20,
							   param1=50, param2=25, minRadius=0, maxRadius=50)



	if (circles is None):
		return img,0

	circles = np.uint16(np.around(circles))
	for i in circles[0, :]:
		# draw the outer circle
		cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
		# draw the center of the circle
		cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

	return cimg, circles



def clean_up_results(data):

	# filter 'noise'
	data = [d for d in data if d.get('size') >= min_area]
	if len(data) == 0:
		return data


	size_list = [t['size'] for t in data]
	top_values = heapq.nlargest(4,size_list)
	avg = np.mean(top_values)
	new_list = [d for d in data if d.get('size') >= avg ]
	new_list = sorted(new_list, key=lambda k: k['size'], reverse=True)

	return new_list


def detectTriangles(img):

	height, width = img.shape[:2]
	response = {"triangles": [], "img_width": int(width) , "img_height": int(height) }

#	img = cv2.medianBlur(img, 5)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#	blurred = cv2.GaussianBlur(gray, (5, 5), 2)


#	thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)
	thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
	contours, h = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	counter = 0

	for cnt in contours:

		approx = cv2.approxPolyDP(cnt,0.2*cv2.arcLength(cnt,True),True)
		area = cv2.contourArea(cnt)

		if len(approx) == 3 :

			m = cv2.moments(cnt)

			try:

				cx = int(m["m10"] / m["m00"])
				cy = int(m["m01"] / m["m00"])

				response["triangles"].append(
					{"x": cx, "y": cy, "size": area, "x_ratio": cx / width, "y_ratio": cy / height, "contours" : cnt})
				counter += 1

			except:
				pass

	if counter > 0:
		clean_list = clean_up_results(response['triangles'])
		response['triangles'] = clean_list
		counter = len(clean_list)


	for item in response['triangles']:
		cv2.drawContours(img, [item['contours']], -1, (0, 255, 0), 2)
		cv2.circle(img, (item['x'], item['y']), 3, (255, 255, 255), -1)

	# clean up contours

	for item in response['triangles']:
		item.pop('contours')


	response["total"] = counter

	return img, thresh, response
