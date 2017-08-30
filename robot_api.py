import paho.mqtt.client as mqtt


class StateBuffer:

	last_command = ''
	current_command = ''

	def __init__(self):
		pass

	def set_command(self, command):
		if command == self.last_command:
			self.current_command = None
		else:
			self.current_command = command
			self.last_command = command

		return self.current_command

	def get_next_command(self):
		return self.current_command


class RobotController:

	# thing_id = 'bob30'
	client = mqtt.Client()

	def __init__(self, thing_id='bob30'):

		self.thing_id = thing_id
		self.client.on_connect = self.handle_connect
		self.client.on_disconnect = self.handle_disconnect
		self.client.connect("127.0.0.1", 1883, 60)
		self.client.loop_start()

	def handle_disconnect(self):
		self.client.loop_stop()

	def handle_connect(self, client, userdata, flags, rc):
		self.client.publish(self.thing_id + '/hw_control', 's')

	def stop_mqtt(self):
		self.send_command('s')
		self.client.loop_stop()

	def send_command(self, command):

		if command is not None:
			self.client.publish(self.thing_id + '/hw_control', command)
