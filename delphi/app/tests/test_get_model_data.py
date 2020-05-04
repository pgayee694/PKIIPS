import unittest
import json

from app import app
from app import global_model_engine
from app.model_engine import ModelEngine
from app.plugins.example_plugins import TestDataAnalyzerPlugin
from app.plugins.example_plugins import TestDataAnalyzerPlugin2

class TestGetModelData(unittest.TestCase):
    """
    Tests the functionality of the '/get-model-data' route/
    """

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        global_model_engine = ModelEngine()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def postDataJson(self, json):
        """Helper method for posting data in the form of JSON."""
        return self.app.post(
            '/update-sensor-data', json=json)

    def postConstraintJson(self, json):
        """Helper method for posting data in the form of JSON."""
        return self.app.post(
            '/update-constraint-data', json=json)

    def getModelData(self):
        """Helper method for getting data in the form of JSON."""
        return self.app.get('/get-model-data').get_json()

    def assertSuccess(self, response):
        """Helper method for asserting a successful response."""
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(as_text=True), '')

    def test_endpoint_no_analyzers(self):
        global_model_engine.start()

        self.assertDictEqual(self.getModelData(), dict())

        global_model_engine.stop()

    def test_endpoint_with_analyzers(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer2 = TestDataAnalyzerPlugin2()
        global_model_engine.add_analyzer(analyzer)
        global_model_engine.add_analyzer(analyzer2)
        global_model_engine.start()

        data_payload = {'increment': 8}
        data_payload2 = {'increment': 2, 'node_id': 1}
        constraint_payload = {'max': 5}
        constraint_payload2 = {'maxsize': 4}

        self.assertDictEqual(self.getModelData(), {'num': 0, 'nodes': []})

        self.assertSuccess(self.postDataJson(data_payload))

        self.assertDictEqual(self.getModelData(), {'num': 8, 'nodes': []})

        self.assertSuccess(self.postDataJson(data_payload2))

        self.assertDictEqual(self.getModelData(), {'num': 10, 'nodes': [1]})

        self.assertSuccess(self.postConstraintJson(constraint_payload))
        self.assertSuccess(self.postConstraintJson(constraint_payload2))

        self.assertDictEqual(self.getModelData(), {'num': 5, 'nodes': [1]})

        global_model_engine.stop()

if __name__ == '__main__':
    unittest.main()