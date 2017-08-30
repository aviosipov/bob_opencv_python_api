import cv2
import paho.mqtt.client as mqtt
import eye_logic
import robot_api
import time


thing_id = 'bob32'
robot_controller = robot_api.RobotController(thing_id=thing_id)



def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))
	client.subscribe( thing_id + '/sensors/camera')


def on_message(client, userdata, msg):
	pass


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

	robot_controller.send_command(eye_logic.RobotCommands.CMD_F)
	time.sleep(10)

	robot_controller.send_command(eye_logic.RobotCommands.CMD_S)
	time.sleep(12)


	robot_controller.send_command(eye_logic.RobotCommands.CMD_B)
	time.sleep(10)


	robot_controller.send_command(eye_logic.RobotCommands.CMD_S)
	time.sleep(12)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

robot_controller.stop_mqtt()
client.loop_stop()
print "stopped MQTT client, app terminated"
