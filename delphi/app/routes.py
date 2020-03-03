from app import app
from flask import request


@app.route('/update-sensor-data', methods=['POST'])
def updateSensorData():
    try:
        data = request.get_json()
        sensorId = int(data.get('id'))
        count = int(data.get('count'))

        # todo: store sensor data
        return '', 204
    except:
        pass

    return 'Invalid Request Syntax', 400
