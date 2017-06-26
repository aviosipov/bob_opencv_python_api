import cv2
import imutils
import argparse


# load image 
image = cv2.imread('images/1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
#thresh = gray



# try to detect shapes 
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)



cnts = cnts[0] if imutils.is_cv2() else cnts[1]

print "I found %d shapes" % (len(cnts))
 
# try to process the shapes 
for c in cnts:
	M = cv2.moments(c)
	cv2.drawContours(image, [c], -1, (0, 255, 0), 2	)


# display the image 
cv2.imshow("Image",thresh)
cv2.imshow("t",image)
cv2.waitKey(0)