import unittest
from delphi.app.graph import *


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

    def test_find_path(self):
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
        fn.calculate_max_flow()
        positive_flow_network = []
        for edge in fn.get_edges():
            if edge.flow >= 0:
                positive_flow_network = positive_flow_network + [edge]
        assert find_path('s', positive_flow_network, 2) == ['s', 'a', 'c', 'b', 'd', 't']
        assert find_path('s', positive_flow_network, 1000) == ['s']
        assert find_path('s', positive_flow_network, 4) == ['s', 'a', 'c', 'b', 'd', 't']


if __name__ == "__main__":
    TestNetworkFlow()
