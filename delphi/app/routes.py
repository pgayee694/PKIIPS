from app import app
from flask import request


@app.route('/')
@app.route('/index')
def index():
    return 'Hello, World!'


@app.route('/update-sensor-data', methods=['POST'])
def updateSensorData():
    data = request.get_json()
    sensorId = data.get('id')
    count = data.get('count')

    if sensorId is not None and isinstance(sensorId, int) and count is not None and isinstance(count, int):
        # todo: store sensor data
        return 'Sensor data saved successfully', 200

    return 'Failed to save sensor data'
