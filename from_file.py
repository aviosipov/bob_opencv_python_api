import cv2
import helpers
import matplotlib.pyplot as plt
import numpy as np

size_list = []

test_files = [ 'images/test_images/photo1.jpg' , 'images/test_images/photo2.jpg', 'images/test_images/photo3.jpg', 'images/test_images/photo4.jpg', 'images/test_images/photo5.jpg',
			   'images/test_images/photo6.jpg','images/test_images/photo7.jpg','images/test_images/photo8.jpg', 'images/test_images/photo9.jpg']

test_files = [ 'images/test_images/photo7.jpg']

for file in test_files:

	img = cv2.imread(file)
	img, thresh, response = helpers.detectTriangles(img)

	print response

	cv2.imshow(file,img)
#	cv2.imshow(file + ' threshold', thresh)

	for item in response['triangles']:
		size_list.append(item['size'])

# plot data for testing
print len(size_list)

plt.plot(size_list,'r--', linewidth=1)
plt.show()

cv2.destroyAllWindows()


