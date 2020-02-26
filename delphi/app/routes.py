from app import app
from flask import request
import cv2
import numpy


@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def upload():
    if request.headers['content-length'] != '0' and request.headers['content-type'] in ['image/jpeg', 'image/png']:
        buf = numpy.frombuffer(request.data, numpy.uint8)
        current_image = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if current_image is None:
            return 'Failed to receive image', 500
        else:
            return 'Image received', 200
    else:
        return 'Request must contain an image', 415
