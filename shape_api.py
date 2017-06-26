# use for shape detection api service 

import os
import cv2
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import helpers
from flask import jsonify

print "api ready ... "
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/hello', methods=['GET'])
def hello():
	return "ok"


@app.route('/upload2', methods=['POST'])
def upload2():
	return "ok"


@app.route('/upload', methods=['POST'])
def upload():
	# Get the name of the uploaded file
	file = request.files['file']
	print("upload request ....")
	print file
	print file.filename

	# Check if the file is one of the allowed types/extensions
	if file and allowed_file(file.filename):
		# Make the filename safe, remove unsupported chars
		filename = secure_filename(file.filename)
		# Move the file form the temporal folder to
		# the upload folder we setup
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER']) + '/' + filename)
		_,_,response = helpers.detectTriangles(img)

		return jsonify(response)

	return "bad file"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', threaded=True)



print "done ..."