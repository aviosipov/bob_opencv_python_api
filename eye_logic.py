class RobotCommands:

	CMD_F = 'f'
	CMD_B = 'b'
	CMD_S = 's'
	CMD_R = 'r'
	CMD_L = 'l'

	def __init__(self):
		pass


class EyeLogic:

	no_data_counter = 0
	offset_trigger = 0.28
	stop_distance = 5500
	no_data_counter_trig = 1
	y_offset_trig = 0.2

	def __init__(self, offset_trigger=0.2, stop_distance=5500, no_data_counter_trig=1):
		self.offset_trigger = offset_trigger
		self.stop_distance = stop_distance
		self.no_data_counter_trig = no_data_counter_trig

	def process_camera_data(self, camera_data):

		response = None

		if len(camera_data['triangles']) == 0:

			response = RobotCommands.CMD_S
			return response

			# if self.no_data_counter >= self.no_data_counter_trig:
			# 	response = RobotCommands.CMD_S
			# else:
			# 	self.no_data_counter += 1
			# return response

		self.no_data_counter = 0
		tr_data = camera_data['triangles'][0]
		x_ratio = float(tr_data['x_ratio'])
		y_ratio = float(tr_data['y_ratio'])
		size = float(tr_data['size'])
		offset = abs(0.5 - x_ratio)

		if y_ratio < self.y_offset_trig:
			return response

		if offset > self.offset_trigger:

			if x_ratio >= 0.5:
				response = RobotCommands.CMD_R

			else:
				response = RobotCommands.CMD_L

		elif size < self.stop_distance:
			response = RobotCommands.CMD_F

		return response


