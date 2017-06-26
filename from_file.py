import numpy as np
import cv2
import helpers


fileName = 'capture/img0101.jpg'
fileName = 'images/3.jpg'
img = cv2.imread(fileName)
img,thresh,response = helpers.detectTriangles(img)

print response

cv2.imshow('img',img)
cv2.imshow('thresh',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()




