"""
Contains classes and utilities for graph operations.
"""

class GraphNode():
    """
    Contains information about each node within the graph representation
    """

    def __init__(self, id_, edges=[], enabled=True):
        """
        Constructs the GraphNode object. Initialized count to 0.

        Params:
            id_: string representing id of the node (room #)
            edges: list of GraphEdge objects with this node as the source
            enabled: if the node is enabled or not
        """

        self.id_ = id_
        self.edges = edges
        self.enabled = enabled
        self.count = 0
    
    def enable(self, enable=True):
        """
        Toggles the availability of a node
        
        Params:
            enable: If the node should be enabled or not
        """

        self.enabled = enable

    def update_count(self, count):
        """
        Updates the count of the node
        
        Params:
            count: the number of people in the node
        """

        self.count = count


class GraphEdge():
    """
    Contains information about each directed edge within the graph representation
    """

    def __init__(self, source, dest, capacity=0):
        """
        Constructs the GraphEdge object.

        Params:
            source: source node
            dest: destination node
            capacity: default capacity of the edge
        """

        self.source = source
        self.dest = dest
        self.capacity = capacity
    
    def update_capacity(self, capacity):
        """
        Updates the capacity of the edge. Cannot be greater than MAX_CAPACITY.

        TODO: Have this do calculations on how to update the capacity rather than just setting it.
        """

        self.capacity = capacity

# TODO: Have this actually populated and easier to access/manipulate
PKI = []