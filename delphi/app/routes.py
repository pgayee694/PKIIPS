from app import app
from flask import request


@app.route('/update-sensor-data', methods=['POST'])
def updateSensorData():
    data = request.get_json(silent=True)

    if data:
        sensorId = data.get('id')
        count = data.get('count')

        if sensorId and isinstance(sensorId, int) and count and isinstance(count, int):
            # todo: store sensor data
            return '', 204

    return 'Invalid Request Syntax', 400
