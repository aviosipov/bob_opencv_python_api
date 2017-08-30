import os
import cv2
import helpers
import eye_logic
import robot_api

capture_folder = 'capture/set7/'
file_list = os.listdir(capture_folder)
logic = eye_logic.EyeLogic()
index = 0

state_buffer = robot_api.StateBuffer()
robot_controller = robot_api.RobotController()

while True:

	img = cv2.imread(capture_folder + file_list[index])
	height, width, channels = img.shape
	img, thresh, response = helpers.detectTriangles(img)

	res = logic.process_camera_data(response)
	last_res = state_buffer.set_command(res)

	robot_controller.send_command(last_res)

	x = ''

	if res == 's':
		x = 's'
	elif res == 'f':
		x = '^'
	elif res == 'r':
		x = '>'
	elif res == 'l':
		x = '<'
	elif res == 'b':
		x = 'bck'

	# draw center line
	cv2.line(img, (width/2, 0), (width/2,height),(150, 150, 150), 1)
	cv2.putText(img, x, (width/2 - 32, 340), cv2.FONT_HERSHEY_SIMPLEX, 2.8, (250, 100, 0), 2)
	cv2.putText(img, file_list[index], (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (20, 25, 20), 2)
	cv2.putText(img, res, (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (150, 255, 250), 2)
	cv2.putText(img, last_res, (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (150, 0, 250), 2)

	# write to file
	# helpers.save_image(img, 'cap_', 'capture/out')

	cv2.imshow('preview', img)
	key = cv2.waitKey(0)

	if 'q' == chr(key & 255):
		break

	elif 't' == chr(key & 255):
		if len(file_list) - index > 1:
			index += 1

	elif 'r' == chr(key & 255):
		index -= 1


cv2.destroyAllWindows()



