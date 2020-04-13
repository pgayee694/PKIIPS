import unittest
from unittest.mock import patch
from app import app
from app.graph import GraphNode, GraphEdge

class TestGetCounts(unittest.TestCase):
    """
    Tests the functionality of the get-counts endpoint
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.patcher = patch('app.routes.PKI', [GraphNode(256), GraphNode(260)])
    
    def tearDown(self):
        self.patcher.stop()
    
    def get(self, room_ids):
        query = ''

        for room in room_ids:
            query += 'room_id={}&'.format(room)

        return self.app.get('/get-counts?{}'.format(query))
    
    def test_get_counts_invalid(self):
        room_ids = [150]
        self.patcher.start()

        resp = self.get(room_ids)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {})
    
    def test_get_counts_individual(self):
        room_ids = [256]
        self.patcher.start()

        resp = self.get(room_ids)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['256'], 0)
    
    def test_get_counts_multiple(self):
        room_ids = [256, 260]
        self.patcher.start()

        resp = self.get(room_ids)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['256'], 0)
        self.assertEqual(resp.get_json()['260'], 0)
