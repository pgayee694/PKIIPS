import unittest
from app.plugins.status_plugin import StatusPlugin

class TestStatusAnalyzerPlugin(unittest.TestCase):
    """
    Tests the Status Analyzer plugin.
    """

    def setUp(self):
        self.analyzer = StatusPlugin()

    def test_constructor(self):
        self.assertSetEqual(self.analyzer.get_constraint_keywords(), set(('node_id',)))
        self.assertSetEqual(self.analyzer.get_data_keywords(), set())

    def test_init(self):
        self.analyzer.init()
        
        self.assertDictEqual(self.analyzer.statuses, dict())

    def test_constraints(self):
        self.analyzer.init()

        self.assertDictEqual(self.analyzer.statuses, dict())

        constraint_payload = {'node_id': '256'}
        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.statuses, {'256': False})

        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.statuses, {'256': True})

        constraint_payload = {'node_id': '10'}
        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.statuses, {'256': True, '10': False})

    def test_collect(self):
        self.analyzer.init()

        self.assertDictEqual(self.analyzer.statuses, dict())

        constraint_payload = {'node_id': '256'}
        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.collect(), {'statuses': {'256': False}})

        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.collect(), {'statuses': {'256': True}})

        constraint_payload = {'node_id': '10'}
        constraint_object = self.analyzer.get_constraint_class()(**constraint_payload)
        self.analyzer.constraint(constraint_object)

        self.assertDictEqual(self.analyzer.collect(), {'statuses': {'256': True, '10': False}})

if __name__ == '__main__':
    unittest.main()