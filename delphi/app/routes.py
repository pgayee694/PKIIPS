from app import app
from app import global_model_engine
from app.graph import GraphEdge, GraphNode, PKI
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

@app.route('/enable/<int:room_id>', methods=['PUT'])
def enable(room_id):
    """
    Enables and disables a node

    Params:
        room_id: id of the node to disable
    """

    data = request.get_json()
    enable = data.get('enable')

    # json bools are lowercases, so need to parse them to python
    if enable == 'True' or enable == 'true':
        enable = True
    elif enable == 'False' or enable == 'false':
        enable = False
    else:
        return jsonify(error='Enable flag not found'), 400

    for room in PKI:
        if room.id_ == room_id:
            room.enable(enable)
            return '', 204
    
    return jsonify(error='Room id not found'), 400

@app.route('/get-counts', methods=['GET'])
def get_counts():
    """
    Gets the count of people in the specified rooms
    """

    rooms = {int(r) for r in request.args.getlist('room_id')}
    counts = {}
    for r in PKI:
        if r.id_ in rooms:
            counts[r.id_] = r.count
    
    return jsonify(counts), 200

@app.route('/get-statuses', methods=['GET'])
def get_statuses():
    """
    Gets the status (enabled/disabled) of the specified rooms
    """

    rooms = {int(r) for r in request.args.getlist('room_id')}
    status = {}
    for r in PKI:
        if r.id_ in rooms:
            status[r.id_] = r.enabled
    
    return jsonify(status), 200
