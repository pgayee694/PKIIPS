
def find_path(start_node, flow, people):
    """
    find_path is a utility function that returns all that nodes that are able to carry flow from a specific source
    node
    :param start_node: The source node to calculate paths for
    :param flow: List of all nodes in the network with positive flow
    :param people: The amount of people that must be carried from the source node
    :return: A list of all possible nodes that contribute to viable paths for start_node
    """
    path_list = [start_node]
    for node in path_list:
        current_node = node
        for edge_check in flow:
            if edge_check.start == current_node and edge_check.end != 'ta':
                if edge_check.flow >= people / 2:
                    if edge_check.end not in path_list:
                        path_list.append(edge_check.end)
    return path_list


class Vertex:
    """
    This is a class representing a node in a graph.

    Attributes:
        name(string): the label given to the node
        source(boolean): true if source, false otherwise
        sink(boolean): true if sink, false otherwise
    """

    def __init__(self, name, source=False, sink=False):
        """
         The constructor for the vertex class

         :param name: the label given to the node
         :param source:true if source, false otherwise
         :param sink: true if sink, false otherwise
        """
        self.name = name
        self.isSource = source
        self.isSink = sink


class Edge:
    """
        This is a class representing a directed edge in a graph.

        Attributes:
            start(string): the node the edge is starting from
            end(string): the node the edge is going to
            capacity(int): How much flow the edge can handle
            flow(int): How much flow the edge ends up carrying
            backwardsEdge(Edge): sister edge in the residual graph
        """

    def __init__(self, start, end, capacity):
        """
        This is the constructor for the Edge class
        :param start: the node the edge is starting from
        :param end: the node the edge is going to
        :param capacity:  How much flow the edge can handle
        """
        self.start = start
        self.end = end
        self.capacity = capacity
        self.flow = 0
        self.backwardsEdge = None


class FlowNetwork:
    """
    FlowNetwork represents a graph of nodes and directed edges, pushing flow from one source to one sink

    Attributes:
        vertices(list): The set of vertices in the flow network
        network(dictionary): A collection of nodes and edges with weights to represent a network flow graph
    """

    def __init__(self):
        """
        The constructor for the FlowNetwork Class
        """
        self.vertices = []
        self.network = {}

    def get_source(self):
        """
        retrieves the source node for the flow network
        :return: the source node
        """
        for vertex in self.vertices:
            if vertex.isSource:
                return vertex
        return None

    def get_sink(self):
        """
        Retrieves the sink node for the flow network
        :return: the sink node
        """
        for vertex in self.vertices:
            if vertex.isSink:
                return vertex
        return None

    def get_vertex(self, name):
        """
        Finds the vertex associated with the name passed in
        :param name: The name associated with the vertex to find
        :return: The vertex represented by name
        """
        for vertex in self.vertices:
            if name == vertex.name:
                return vertex

    def vertex_in_network(self, name):
        """
        Decides if a vertex is in the network based off of name
        :param name: The name of the vertex to check for
        :return: True if the vertex is already in the network; false otherwise
        """
        for vertex in self.vertices:
            if vertex.name == name:
                return True
        return False

    def get_edges(self):
        """
        Retrieves all the edges in the network
        :return: The edges in the network
        """
        all_edges = []
        for vertex in self.network:
            for edge_check in self.network[vertex]:
                all_edges.append(edge_check)
        return all_edges

    def add_vertex(self, name, isSource=False, isSink=False):
        """
        Adds a vertex to the flow network
        :param name: The identifier to be associated with the node
        :param isSource: True if it's a source node, false otherwise
        :param isSink: True if it's a sink node, false otherwise
        :return: False if error
        """
        if isSource is True and isSink is True:
            return False

        if self.vertex_in_network(name):
            return False

        if isSource:
            if self.get_source() is not None:
                return False

        if isSink:
            if self.get_sink() is not None:
                return False

        new_vertex = Vertex(name, isSource, isSink)
        self.vertices.append(new_vertex)
        self.network[new_vertex.name] = []

    def add_edge(self, start, end, capacity):
        """
        Adds a directed edge to the flow network
        :param start: The node the edge is directed out of
        :param end: The node the edge is directed into
        :param capacity: The initial amount that can flow through the edge
        :return: False if error
        """
        if start == end:
            return False

        if not self.vertex_in_network(start):
            return False

        if not self.vertex_in_network(end):
            return False

        for edge_check in self.get_edges():
            if edge_check.start == start and edge_check.end == end and edge_check.capacity == capacity:
                return False

        new_edge = Edge(start, end, capacity)
        return_edge = Edge(end, start, 0)
        new_edge.backwardsEdge = return_edge
        return_edge.backwardsEdge = new_edge
        vertex = self.get_vertex(start)
        self.network[vertex.name].append(new_edge)
        return_vertex = self.get_vertex(end)
        self.network[return_vertex.name].append(return_edge)

    def get_path(self, start, end, path):
        """
        Finds a path from a start node to an end node
        :param start: the node to start searching from
        :param end: The node to arrive at
        :param path: The set of nodes and edges to look for a path through
        :return: the found path
        """
        if start == end:
            return path

        for edge_check in self.network[start]:
            residual_capacity = edge_check.capacity - edge_check.flow
            if residual_capacity > 0 and not (edge_check, residual_capacity) in path:
                result = self.get_path(edge_check.end, end, path + [(edge_check, residual_capacity)])
                if result is not None:
                    return result

    def calculate_max_flow(self):
        """
        Calculates the max flow of the flow network using the Ford-Fulkerson algorithm
        :return: and integer representing the max flow
        """
        source = self.get_source()
        sink = self.get_sink()
        if source is None or sink is None:
            return "Network does not have source and sink"
        path = self.get_path(source.name, sink.name, [])
        while path is not None:
            flow = min(edge[1] for edge in path)
            for edge, res in path:
                edge.flow += flow
                edge.backwardsEdge.flow -= flow
            path = self.get_path(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])




