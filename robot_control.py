import cv2
import paho.mqtt.client as mqtt
import redis
import pickle
import logging
import eye_logic
import robot_api

camera_logic = eye_logic.EyeLogic()
state_buffer = robot_api.StateBuffer()
robot_controller = robot_api.RobotController()
r = redis.StrictRedis(host='localhost', port=6379, db=0)
thing_id = 'bob30'
logging.basicConfig()


def process_camera_data():

	camera_data = pickle.loads(r.get(thing_id))
	res = camera_logic.process_camera_data(camera_data)
	last_res = state_buffer.set_command(res)
	robot_controller.send_command(last_res)


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe( thing_id + '/sensors/camera')


def on_message(client, userdata, msg):
	# handle_mqtt_message(msg.payload)
	process_camera_data()


def on_disconnect(client, userdata,rc=0):
	print "stop loop, disconnected for broker"
	client.loop_stop()


client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect("127.0.0.1", 1883, 60)
client.loop_start()


tmp_img = cv2.imread('images/qrcode.jpg')
cv2.namedWindow("window")
cv2.imshow("window", tmp_img)


while True:
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

robot_controller.stop_mqtt()
client.loop_stop()
print "stopped MQTT client, app terminated"
