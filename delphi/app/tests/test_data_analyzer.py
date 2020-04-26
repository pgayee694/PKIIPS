import unittest
from app.plugins.example_plugins import TestDataAnalyzerPlugin
from app import data_analyzer

class TestDataAnalyzer(unittest.TestCase):
    """
    Tests inheriting and using a DataAnalyzer
    """

    def test_constructor(self):
        analyzer = TestDataAnalyzerPlugin()

        self.assertIn('increment', analyzer.get_data_keywords())
        self.assertIn('max', analyzer.get_constraint_keywords())
        
    def test_init(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

    def test_collect(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        data_payload = {'increment': 1}
        data_object = analyzer.get_data_class()(**data_payload)

        self.assertEqual(analyzer.collect()['num'], 0)
        analyzer.analyze(data_object)
        self.assertEqual(analyzer.collect()['num'], 1)

    def test_analyze_constraint(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        data_payload        = {'increment': 10}
        constraint_payload  = {'max': 5}
        data_object         = analyzer.get_data_class()(**data_payload)
        constraint_object   = analyzer.get_constraint_class()(**constraint_payload)

        analyzer.analyze(data_object)
        self.assertEqual(analyzer.collect()['num'], 10)

        analyzer.constraint(constraint_object)
        self.assertEqual(analyzer.collect()['num'], 5)

    def test_shutdown(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        data_payload = {'increment': 10}
        data_object  = analyzer.get_data_class()(**data_payload)

        analyzer.analyze(data_object)
        analyzer.shutdown()

        self.assertEqual(analyzer.num, -1)