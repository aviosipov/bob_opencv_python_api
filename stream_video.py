#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import StringIO

app = Flask(__name__)
prev_frame = ''



@app.route('/')
def index():
    return render_template('./index.html')

def gen():
    while True:
        frame = cv2.imread('uploads/bob30.jpg')

        try:

            ret, jpeg = cv2.imencode('.jpg', frame)
            t = jpeg.tobytes()
            prev_frame = t

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + t + b'\r\n\r\n')



        except cv2.error as e:

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + prev_frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)