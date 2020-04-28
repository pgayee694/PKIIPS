import unittest
from app.plugins.example_plugins import TestDataAnalyzerPlugin
from app.plugins.example_plugins import TestDataAnalyzerPlugin2
from app.data_analyzer import DataAnalyzerPlugin
from app.model_engine import ModelEngine

class TestModelEngine(unittest.TestCase):
    """
    Tests the ModelEngine class.
    """

    def test_constructor(self):
        engine = ModelEngine()

        self.assertListEqual(engine.analyzers, [])

    def test_add_analyzer(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        engine.add_analyzer(analyzer)

        self.assertListEqual(engine.analyzers, [analyzer])

    def test_start(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        engine.add_analyzer(analyzer)

        engine.start()
        
        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

    def test_stop(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        engine.add_analyzer(analyzer)

        engine.start()

        self.assertEqual(analyzer.num, 0)

        engine.stop()

        self.assertEqual(analyzer.num, -1)

    def test_update_data(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        analyzer2 = TestDataAnalyzerPlugin2()

        engine.add_analyzer(analyzer)
        engine.add_analyzer(analyzer2)

        engine.start()

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'increment': 5}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 2}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set((2,)))
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 5, 'extra': 1, 'increment': 4}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 9)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 1)
        self.assertSetEqual(analyzer2.nodes, set((2, 5)))
        self.assertIsNone(analyzer2.maxsize)

        engine.stop()

        self.assertEqual(analyzer.num, -1)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 1)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

    def test_update_constraint(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        analyzer2 = TestDataAnalyzerPlugin2()

        engine.add_analyzer(analyzer)
        engine.add_analyzer(analyzer2)

        engine.start()

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'increment': 5}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 2}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set((2,)))
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 5, 'extra': 1, 'increment': 4}
        constraint_payload = {'max': 8, 'maxsize': 1}

        engine.update_constraint(constraint_payload)
        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 8)
        self.assertEqual(analyzer.max, 8)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set((2,)))
        self.assertEqual(analyzer2.maxsize, 1)

        engine.stop()

        self.assertEqual(analyzer.num, -1)
        self.assertEqual(analyzer.max, 8)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertEqual(analyzer2.maxsize, 1)

    def test_collect(self):
        engine = ModelEngine()
        analyzer = TestDataAnalyzerPlugin()
        analyzer2 = TestDataAnalyzerPlugin2()

        engine.add_analyzer(analyzer)
        engine.add_analyzer(analyzer2)

        engine.start()

        self.assertEqual(analyzer.num, 0)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'increment': 5}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 2}

        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 5)
        self.assertIsNone(analyzer.max)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set((2,)))
        self.assertIsNone(analyzer2.maxsize)

        data_payload = {'node_id': 5, 'extra': 1, 'increment': 4}
        constraint_payload = {'max': 8, 'maxsize': 1}

        engine.update_constraint(constraint_payload)
        engine.update_data(data_payload)

        self.assertEqual(analyzer.num, 8)
        self.assertEqual(analyzer.max, 8)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set((2,)))
        self.assertEqual(analyzer2.maxsize, 1)

        self.assertDictEqual(engine.collect(), {'nodes': set((2,)), 'num': 8})

        engine.stop()

        self.assertEqual(analyzer.num, -1)
        self.assertEqual(analyzer.max, 8)

        self.assertEqual(analyzer2.num, 0)
        self.assertSetEqual(analyzer2.nodes, set())
        self.assertEqual(analyzer2.maxsize, 1)