import unittest

from app import app
from app import global_model_engine
from app.model_engine import ModelEngine
from app.plugins.example_plugins import TestDataAnalyzerPlugin
from app.plugins.example_plugins import TestDataAnalyzerPlugin2

class TestUploadConstraintData(unittest.TestCase):
    """
    Tests the functionality of the '/update-constraint-data' route.
    """

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
            '/update-constraint-data', data=data)

    def postDataJson(self, json):
        """Helper method for posting data in the form of JSON."""
        return self.app.post(
            '/update-sensor-data', json=json)

    def postConstraintJson(self, json):
        """Helper method for posting data in the form of JSON."""
        return self.app.post(
            '/update-constraint-data', json=json)

    def assertSuccess(self, response):
        """Helper method for asserting a successful response."""
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_data(as_text=True), '')

    def assertFailure(self, response):
        """Helper method for asserting an unsuccessful response."""
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_data(as_text=True),
                         'Invalid Request Syntax')

    def test_endpoint_success(self):
        self.assertSuccess(self.postConstraintJson({"max": 15}))

    def test_endpoint_failure(self):
        self.assertFailure(self.postData("max: 15"))
        self.assertFailure(self.postData(dict(max=15)))

    def test_model_engine(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer2 = TestDataAnalyzerPlugin2()
        global_model_engine.add_analyzer(analyzer)
        global_model_engine.add_analyzer(analyzer2)
        global_model_engine.start()

        data_payload = {'increment': 8}
        constraint_payload = {'max': 5}
        constraint_payload2 = {'maxsize': 4}

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

        self.assertSuccess(self.postDataJson(data_payload))

        self.assertEqual(analyzer.num, 8)
        self.assertIsNone(analyzer.max)

        self.assertSuccess(self.postConstraintJson(constraint_payload))

        self.assertEqual(analyzer.num, 5)
        self.assertEqual(analyzer.max, 5)

        self.assertDictEqual(analyzer.collect(), {'num': 5})

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        self.assertSuccess(self.postConstraintJson(constraint_payload2))

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertEqual(analyzer2.maxsize, 4)