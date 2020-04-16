import unittest
from unittest.mock import patch
from app import app
from app.graph import GraphNode, GraphEdge

class TestEnable(unittest.TestCase):
    """
    Tests the enable PUT endpoint
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.patcher = patch('app.routes.PKI', [GraphNode(256)])

    def tearDown(self):
        self.patcher.stop()

    def put(self, json, room_id):
        return self.app.put('/enable/{}'.format(room_id), json=json)
    
    def test_enable_valid(self):
        json = {"enable": "true"}
        room_id = 256
        self.patcher.start()

        resp = self.put(json, room_id)
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(resp.get_data(as_text=True), '')
    
    def test_enable_no_flag(self):
        json = {}
        room_id = 256
        self.patcher.start()

        resp = self.put(json, room_id)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['error'], 'Enable flag not found')
    
    def test_invalid_room(self):
        json = {"enable": "false"}
        room_id = 260
        self.patcher.start()

        resp = self.put(json, room_id)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json()['error'], 'Room id not found')
