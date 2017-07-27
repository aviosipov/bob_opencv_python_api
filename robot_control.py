import paho.mqtt.client as mqtt
import redis
import pickle
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from time import sleep
import cv2

robot_command_interval = 0.005
robot_drive_delay = 0.0
robot_turn_delay = 0.0
offset_trigger = 0.25

robot_stop_distance = 2000

no_data_counter = 0
no_data_counter_trig = 20

r = redis.StrictRedis(host='localhost', port=6379, db=0)
thing_id = 'bob30'
last_command = ''

logging.basicConfig()


def handle_mqtt_message(data):
	camera_data = pickle.loads(data)
	process_camera_data()


def process_camera_data():

	camera_data = pickle.loads(r.get(thing_id))

	global no_data_counter
	global last_command

	if len(camera_data['triangles']) == 0:

		if no_data_counter >= no_data_counter_trig and last_command != 's':
			client.publish(thing_id + '/hw_control', 's')
			last_command = 's'
			print 's'

		else:
			no_data_counter += 1
		return

	no_data_counter = 0
	tr_data = camera_data['triangles'][0]
	x_ratio = float(tr_data['x_ratio'])
	size = float(tr_data['size'])
	offset = abs ( 0.5 - x_ratio )

	if offset > offset_trigger :

		if x_ratio >= 0.5 and last_command != 'r':
			client.publish(thing_id + '/hw_control', 'r')
			last_command = 'r'
			print 'r ' + str(x_ratio)

		elif last_command != 'l':
			client.publish(thing_id + '/hw_control', 'l')
			last_command = 'l'
			print 'l ' + str(x_ratio)

	elif size < robot_stop_distance and last_command != 'f':
		client.publish(thing_id + '/hw_control', 'f')
		last_command = 'f'
		print 'f' + str(size)


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe( thing_id + '/sensors/camera')
	client.publish(thing_id + '/hw_control', 's')


def on_message(client, userdata, msg):
	handle_mqtt_message(msg.payload)


def on_disconnect(client, userdata,rc=0):
	print "stop loop, disconnected for broker"
	client.loop_stop()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("127.0.0.1", 1883, 60)
client.loop_start()

# scheduler = BackgroundScheduler()
# scheduler.start()
# scheduler.add_job(process_camera_data, 'interval', seconds=robot_command_interval)


tmp_img = cv2.imread('images/qrcode.jpg')
cv2.namedWindow("window")
cv2.imshow("window", tmp_img)


while True:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break


client.loop_stop()
# scheduler.shutdown()

print "stopped MQTT client, app terminated"