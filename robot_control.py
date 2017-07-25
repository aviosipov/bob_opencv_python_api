import paho.mqtt.client as mqtt
import redis
import pickle
from apscheduler.schedulers.background import BackgroundScheduler
import logging



r = redis.StrictRedis(host='localhost', port=6379, db=0)
thing_id = 'bob30'

logging.basicConfig()


def handle_mqtt_message(data):
    camera_data = pickle.loads(data)


def process_camera_data():

    camera_data = pickle.loads(r.get(thing_id))

    if len(camera_data['triangles']) == 0:
        client.publish(thing_id + '/hw_control', 'b')
        return


    tr_data = camera_data['triangles'][0]

    x_ratio = float(tr_data['x_ratio'])
    size = float(tr_data['size'])


    print size

    offset = abs ( 0.5 - x_ratio )


    if (offset > 0.05) :

        if (x_ratio >= 0.5):
            client.publish(thing_id + '/hw_control', 'r')
            print 'l ' + str(x_ratio)

        else:
            client.publish(thing_id + '/hw_control', 'l')
            print 'r ' + str(x_ratio)

    elif (size < 15000):

        client.publish(thing_id + '/hw_control', 'f')
        print 'f' + str(size)




def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("bob30/#")


def on_message(client, userdata, msg):
    if (msg.topic == thing_id +'/hw_control'):return
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

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(process_camera_data, 'interval', seconds=.15)



try:
    while True:
        pass


except KeyboardInterrupt:
    pass



client.loop_stop()
scheduler.shutdown()


print "stopped MQTT client, app terminated"
