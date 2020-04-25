import unittest
from app.plugins.test_plugins import TestDataAnalyzerPlugin
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

        self.assertEqual(analyzer.collect()['num'], 0)
        analyzer.analyze(data_analyzer.DataContainer({'increment': 1}))
        self.assertEqual(analyzer.collect()['num'], 1)

    def test_analyze_constraint(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        analyzer.analyze(data_analyzer.DataContainer({'increment': 10}))
        self.assertEqual(analyzer.collect()['num'], 10)

        analyzer.analyze(data_analyzer.DataContainer({'not_increment': 1}))
        self.assertEqual(analyzer.collect()['num'], 10)

        analyzer.constraint(data_analyzer.ConstraintsContainer({'max': 5}))
        self.assertEqual(analyzer.collect()['num'], 5)

        analyzer.constraint(data_analyzer.ConstraintsContainer({'not_max': 1}))
        self.assertEqual(analyzer.collect()['num'], 5)

    def test_shutdown(self):
        analyzer = TestDataAnalyzerPlugin()
        analyzer.init()

        analyzer.analyze(data_analyzer.DataContainer({'increment': 10}))
        analyzer.shutdown()

        self.assertEqual(analyzer.num, -1)

class TestDataContainer(unittest.TestCase):
    """
    Tests a DataContainer
    """

    def test_constructor(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.DataContainer(data)

        self.assertEqual(container.data, data)

    def test_get(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.DataContainer(data)

        self.assertEqual(container.get('test'), data['test'])
        self.assertEqual(container.get('test2'), data['test2'])
        self.assertEqual(container['test'], data['test'])
        self.assertEqual(container['test2'], data['test2'])
        self.assertIsNone(container.get('hello'))
        self.assertIsNone(container['hello'])

    def test_contains_keyword(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.DataContainer(data)

        self.assertTrue(container.contains_keyword('test'))
        self.assertTrue(container.contains_keyword('test2'))
        self.assertFalse(container.contains_keyword('test3'))

class TestConstraintsContainer(unittest.TestCase):
    """
    Tests a ConstraintsContainer
    """

    def test_constructor(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.ConstraintsContainer(data)

        self.assertEqual(container.data, data)

    def test_get(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.ConstraintsContainer(data)

        self.assertEqual(container.get('test'), data['test'])
        self.assertEqual(container.get('test2'), data['test2'])
        self.assertEqual(container['test'], data['test'])
        self.assertEqual(container['test2'], data['test2'])
        self.assertIsNone(container.get('hello'))
        self.assertIsNone(container['hello'])

    def test_contains_keyword(self):
        data = {'test': 12, 'test2': 'hello'}
        container = data_analyzer.ConstraintsContainer(data)

        self.assertTrue(container.contains_keyword('test'))
        self.assertTrue(container.contains_keyword('test2'))
        self.assertFalse(container.contains_keyword('test3'))