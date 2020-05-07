from app import app
from app import global_model_engine
from flask import request, jsonify

@app.route('/update-sensor-data', methods=['POST'])
def updateSensorData():
    """
    Endpoint for updating the data of the data analyzers.
    This endpoint is used by a Seer to deliver data.
    """
    try:
        data = request.get_json()
        if data is not None:
            global_model_engine.update_data(data)
            return '', 204
    except:
        pass

    return 'Invalid Request Syntax', 400

@app.route('/update-constraint-data', methods=['POST'])
def updateConstraintData():
    """
    Endpoint for updating the constraints of the data analyzers.
    This endpoint is used by an Oracle to deliver constraints.
    """
    try:
        data = request.get_json()
        if data is not None:
            global_model_engine.update_constraint(data)
            return '', 204
    except:
        pass

    return 'Invalid Request Syntax', 400

@app.route('/get-model-data', methods=['GET'])
def getModelData():
    return jsonify(global_model_engine.collect())