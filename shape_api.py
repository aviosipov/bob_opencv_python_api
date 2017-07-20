# use for shape detection api service 

import os
import cv2
from flask import Flask, request, redirect, url_for,render_template,Response
from werkzeug.utils import secure_filename
import helpers
from flask import jsonify
import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt
import json

print "api ready ... "

UPLOAD_FOLDER = 'uploads'


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MQTT_BROKER_URL'] = '127.0.0.1'
app.config['MQTT_BROKER_PORT'] = 1883
mqtt = Mqtt(app)

live_image = None


# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']






@app.route('/live')
def index():
	return render_template('./index.html')

def gen():
	while True:

		try:

			frame = live_image
			ret, jpeg = cv2.imencode('.jpg', frame)
			t = jpeg.tobytes()

			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + t + b'\r\n\r\n')

		except cv2.error as e:
			print "bad file?"




@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

















@app.route('/upload', methods=['POST'], defaults={'thing_id': 'bob30'})
@app.route('/upload/<thing_id>', methods=['POST'] )
def upload(thing_id):

	print "thing id:" + thing_id

	# Get the name of the uploaded file
	file = request.files['file']
	print("upload request ....")
	print file
	print file.filename

	# Check if the file is one of the allowed types/extensions
	if file and allowed_file(file.filename):

		filename=thing_id+'.jpg'
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER']) + '/' + filename)
		img = helpers.rotate(img,270)
		_,_,response = helpers.detectTriangles(img)

		global live_image
		live_image = img

		mqtt.publish(thing_id + '/sensors/camera', payload=json.dumps(response))
		return jsonify(response)

	return "bad file"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', threaded=True)


print "done ..."
