from __future__ import division
import numpy as np
import cv2
import json



def detectTriangles(img):

	height, width = img.shape[:2]
	response = {"triangles": [], "img_width": int(width) , "img_height": int(height) }

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)

	ret, thresh = cv2.threshold(blurred,127,255,cv2.THRESH_BINARY)
	contours, h = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

	counter = 0

	for cnt in contours:

		approx = cv2.approxPolyDP(cnt,0.2*cv2.arcLength(cnt,True),True)
		area = cv2.contourArea(cnt)

		if len(approx) == 3:

			m = cv2.moments(cnt)
			cx = int(m["m10"] / m["m00"])
			cy = int(m["m01"] / m["m00"])

			cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)
			cv2.drawContours(img,[cnt],-1,(0,255,0),2)

			response["triangles"].append({"x": cx, "y": cy, "size": area, "x_ratio": cx/width, "y_ratio": cy/height})
			counter += 1

	response["total"] = counter

	return img, thresh, response
