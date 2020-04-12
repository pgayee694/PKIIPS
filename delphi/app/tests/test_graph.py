import unittest
from app.graph import GraphNode, GraphEdge

class TestGraph(unittest.TestCase):
    """
    Tests the functionality of the graph module
    """

    def test_enable_false(self):
        enable = False
        node = GraphNode(256)

        node.enable(enable)
        
        actual = node.enabled
        self.assertFalse(actual)
    
    def test_enable_true(self):
        node = GraphNode(256, [], False)

        node.enable()

        actual = node.enabled
        self.assertTrue(actual)
    
    def test_update_count(self):
        count = 12
        node = GraphNode(256)
        
        node.update_count(count)

        actual = node.count
        self.assertEqual(actual, count)
    
    def test_update_capacity(self):
        capacity = 15
        edge = GraphEdge(GraphNode(256), GraphNode(260), 20)

        edge.update_capacity(15)

        actual = edge.capacity
        self.assertEqual(actual, capacity)
