import unittest
from app.graph import *
from app.pki_model import PKI
from app.plugins.graph_plugin import GraphPlugin


class TestGraphPlugin(unittest.TestCase):
    """
        Tests for the graph plugin
        """

    def test_constructor(self):
        analyzer = GraphPlugin()
        assert analyzer.get_data_keywords() == {'Count', 'Room'}
        self.assertIn('node_id', analyzer.get_constraint_keywords())

    def test_init(self):
        analyzer = GraphPlugin()
        analyzer.init()

        self.assertIsNotNone(analyzer.pki)
        self.assertEqual(analyzer.routes, {})

    def test_collect(self):
        analyzer = GraphPlugin()
        analyzer.init()

        data_payload = {'Room': '252', 'Count': 25}
        data_object = analyzer.get_data_class()(**data_payload)

        self.assertEqual(analyzer.collect(), {'paths': {}})
        analyzer.analyze(data_object)
        self.assertEqual(analyzer.collect(),
                         {'paths': {'252': ['252', 'h1', 'h2', 'h5', 't2'],
                                    '256': ['256', 'h1', 'h2', 'h5', 't2'],
                                    '260': ['260', 'h1', 'h2', 'h5', 't2']}})

        data_payload = {'Room': '252', 'Count': 20}
        data_object = analyzer.get_data_class()(**data_payload)
        analyzer.analyze(data_object)
        self.assertEqual(analyzer.collect(),
                         {'paths': {'252': ['252', 'h1', 'h2', 'h5', 't2'],
                                    '256': ['256', 'h1', 'h2', 'h5', 't2'],
                                    '260': ['260', 'h1', 'h2', 'h5', 't2']}})

    def test_analyze_constraint(self):
        analyzer = GraphPlugin()
        analyzer.init()

        data_payload = {'Room': '252', 'Count': 25}
        constraint_payload = {'node_id': 't2'}
        data_object = analyzer.get_data_class()(**data_payload)
        constraint_object = analyzer.get_constraint_class()(**constraint_payload)

        analyzer.analyze(data_object)
        self.assertEqual(analyzer.collect(),
                         {'paths': {'252': ['252', 'h1', 'h2', 'h5', 't2'],
                                    '256': ['256', 'h1', 'h2', 'h5', 't2'],
                                    '260': ['260', 'h1', 'h2', 'h5', 't2']}})

        analyzer.constraint(constraint_object)
        self.assertEqual(analyzer.collect(), {'paths': {'252': ['252', 'h1', 'h2', 't1'],
           '256': ['256'],
           '260': ['260', 'h6', 'h4']}})

    def test_shutdown(self):
        analyzer = GraphPlugin()
        analyzer.init()

        data_payload = {'Room': '252', 'Count': 25}
        data_object = analyzer.get_data_class()(**data_payload)

        analyzer.analyze(data_object)
        analyzer.shutdown()

        self.assertIsNone(analyzer.pki)


class TestPKI(unittest.TestCase):
    """
    Tests for the PKI model
    """

    def test_toggle(self):
        pki = PKI()
        assert pki.toggle('h1') == {'h1': False}
        assert pki.toggle('h1') == {'h1': True}

    def test_update_room(self):
        pki = PKI()
        assert pki.edge_levels == {'l1': {'sa': [('252', 1000), ('256', 1000), ('260', 1000)], '252': [('h1', 25)],
                                          '256': [('h1', 30)], '260': [('h1', 20)], 'h1': [('h2', 80)],
                                          'h2': [('h5', 75), ('t1', 25)], 't1': [('ta', 1000)], 't2': [('ta', 1000)],
                                          'h5': [('t2', 80)]},
                                   'l2': {'252': [('h1', 12.5), ('h3', 12.5)], 'h3': [('h4', 20)],
                                          'h4': [('t3', 20), ('t4', 20)], 't3': [('ta', 1000)], 't4': [('ta', 1000)],
                                          'h1': [('h2', 80), ('h3', 40)]},
                                   'l3': {'260': [('h1', 10.0), ('h6', 10.0)], 'h6': [('h4', 30)]}}
        pki.update_room('252', 30)
        assert pki.edge_levels == {'l1': {'sa': [('252', 1000), ('256', 1000), ('260', 1000)], '252': [('h1', 30)],
                                          '256': [('h1', 30)], '260': [('h1', 20)], 'h1': [('h2', 80)],
                                          'h2': [('h5', 75), ('t1', 25)], 't1': [('ta', 1000)], 't2': [('ta', 1000)],
                                          'h5': [('t2', 80)]},
                                   'l2': {'252': [('h1', 15.0), ('h3', 15.0)], 'h3': [('h4', 20)],
                                          'h4': [('t3', 20), ('t4', 20)], 't3': [('ta', 1000)], 't4': [('ta', 1000)],
                                          'h1': [('h2', 80), ('h3', 40)]},
                                   'l3': {'260': [('h1', 10.0), ('h6', 10.0)], 'h6': [('h4', 30)]}}


class TestNetworkFlow(unittest.TestCase):
    """
    Tests the functionality of the NetworkFlow class
    """

    def test_add_vertex(self):
        fn = FlowNetwork()
        fn.add_vertex('s', True, False)
        fn.add_vertex('t', False, True)
        fn.add_vertex('a', False, False)
        fn.add_vertex('b', False, False)
        fn.add_vertex('c', False, False)
        fn.add_vertex('d', False, False)
        self.assertTrue(fn.vertices)
        assert len(fn.vertices) == 6

    def test_add_edge(self):
        fn = FlowNetwork()
        fn.add_vertex('s', True, False)
        fn.add_vertex('t', False, True)
        fn.add_vertex('a', False, False)
        fn.add_vertex('b', False, False)
        fn.add_vertex('c', False, False)
        fn.add_vertex('d', False, False)
        fn.add_edge('s', 'a', 4)
        fn.add_edge('a', 'b', 4)
        fn.add_edge('b', 't', 2)
        fn.add_edge('s', 'c', 3)
        fn.add_edge('c', 'd', 6)
        fn.add_edge('d', 't', 6)
        fn.add_edge('b', 'c', 3)
        self.assertTrue(fn.network)
        assert len(fn.network) == 6

    def test_calculate_max_flow(self):
        fn = FlowNetwork()
        assert fn.calculate_max_flow() == "Network does not have source and sink"
        fn.add_vertex('s', True, False)
        fn.add_vertex('t', False, True)
        assert fn.calculate_max_flow() == 0
        fn.add_vertex('a', False, False)
        fn.add_vertex('b', False, False)
        fn.add_vertex('c', False, False)
        fn.add_vertex('d', False, False)
        assert fn.calculate_max_flow() == 0
        fn.add_edge('s', 'a', 4)
        fn.add_edge('a', 'b', 4)
        fn.add_edge('b', 't', 2)
        assert fn.calculate_max_flow() == 2
        fn.add_edge('s', 'c', 3)
        fn.add_edge('c', 'd', 6)
        fn.add_edge('d', 't', 6)
        assert fn.calculate_max_flow() == 5
        fn.add_edge('b', 'c', 3)
        assert fn.calculate_max_flow() == 7


if __name__ == "__main__":
    TestNetworkFlow()
    TestPKI()
    TestGraphPlugin()
