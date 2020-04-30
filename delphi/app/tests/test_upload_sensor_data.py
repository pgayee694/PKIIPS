import unittest

from app import app
from app import global_model_engine
from app.model_engine import ModelEngine
from app.plugins.example_plugins import TestDataAnalyzerPlugin

class TestUploadSensorData(unittest.TestCase):
    """Tests the functionality of the '/update-sensor-data' route."""

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        global_model_engine = ModelEngine()
        self.app = app.test_client()

    def tearDown(self):
        pass

    def postData(self, data):
        """Helper method for posting data in the form of a string or a dict."""
        return self.app.post(
            '/update-sensor-data', data=data)

    def postJson(self, json):
        """Helper method for posting data in the form of JSON."""
        return self.app.post(
            '/update-sensor-data', json=json)

    def assertSuccess(self, response):
        """Helper method for asserting a successful response."""
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(as_text=True), '')

    def assertFailure(self, response):
        """Helper method for asserting an unsuccessful response."""
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True),
                         'Invalid Request Syntax')

    def test_zero_id_and_count(self):
        self.assertSuccess(self.postJson({"id": 0, "count": 0}))
        self.assertSuccess(self.postJson({"id": 0, "count": 1}))
        self.assertSuccess(self.postJson({"id": 1, "count": 0}))

    def test_negative_id_and_count(self):
        self.assertSuccess(self.postJson({"id": -1, "count": -1}))
        self.assertSuccess(self.postJson({"id": -1, "count": 1}))
        self.assertSuccess(self.postJson({"id": 1, "count": -1}))

    def test_int_id_and_count(self):
        self.assertSuccess(self.postJson({"id": 1, "count": 1}))

    def test_int_id_and_str_count(self):
        self.assertSuccess(self.postJson({"id": 1, "count": "1"}))

    def test_str_id_and_count(self):
        self.assertSuccess(self.postJson({"id": "1", "count": "1"}))

    def test_str_id_and_int_count(self):
        self.assertSuccess(self.postJson({"id": "1", "count": 1}))

    def test_additional_fields(self):
        self.assertSuccess(self.postJson({"id": "1", "count": 1, "rand": 0.1}))

    def test_non_json(self):
        self.assertFailure(self.postData('test'))
        self.assertFailure(self.postData(dict(id=0, count=0)))

    def test_model_engine(self):
        analyzer = TestDataAnalyzerPlugin()
        global_model_engine.add_analyzer(analyzer)
        global_model_engine.start()
        data_payload = {'increment': 5}

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

        self.assertSuccess(self.postJson(data_payload))

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

if __name__ == '__main__':
    unittest.main()
