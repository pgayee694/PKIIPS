
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
        self.source = source
        self.sink = sink


class Edge:
    """
        This is a class representing a directed edge in a graph.

        Attributes:
            start(string): the node the edge is starting from
            end(string): the node the edge is going to
            capacity(int): How much flow the edge can handle
            flow(int): How much flow the edge ends up carrying
            returnEdge(Edge): sister edge in the residual graph
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
        self.returnEdge = None


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
            if vertex.source:
                return vertex
        return None

    def get_sink(self):
        """
        Retrieves the sink node for the flow network
        :return: the sink node
        """
        for vertex in self.vertices:
            if vertex.sink:
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

    def add_vertex(self, name, source=False, sink=False):
        """
        Adds a vertex to the flow network
        :param name: The identifier to be associated with the node
        :param source: True if it's a source node, false otherwise
        :param sink: True if it's a sink node, false otherwise
        :return: Returns a string if error, nothing otherwise
        """
        if source is True and sink is True:
            return "Vertex cannot be source and sink"
        if self.vertex_in_network(name):
            return "ERROR"
        if source:
            if self.get_source() is not None:
                return "ERROR"
        if sink:
            if self.get_sink() is not None:
                return "ERROR"
        new_vertex = Vertex(name, source, sink)
        self.vertices.append(new_vertex)
        self.network[new_vertex.name] = []

    def add_edge(self, start, end, capacity):
        """
        Adds a directed edge to the flow network
        :param start: The node the edge is directed out of
        :param end: The node the edge is directed into
        :param capacity: The initial amount that can flow through the edge
        :return: string if error occurs, nothing otherwise
        """
        if start == end:
            return "Cannot have same start and end"
        if not self.vertex_in_network(start):
            return "Start vertex has not been added yet"
        if not self.vertex_in_network(end):
            return "End vertex has not been added yet"
        for edge_check in self.get_edges():
            if edge_check.start == start and edge_check.end == end and edge_check.capacity == capacity:
                return "STOP"
        new_edge = Edge(start, end, capacity)
        return_edge = Edge(end, start, 0)
        new_edge.returnEdge = return_edge
        return_edge.returnEdge = new_edge
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
                edge.returnEdge.flow -= flow
            path = self.get_path(source.name, sink.name, [])
        return sum(edge.flow for edge in self.network[source.name])


def run_optimization(PKI_model):
    """
    The main program which builds a network flow graph and then runs a network flow algorithm to insure all
    flow desired makes it through the network
    :return: n/a
    """
    # for iterating through while loop
    level_count = 1
    # create empty graph
    opt_graph = FlowNetwork()

    # add artificial source and sink
    opt_graph.add_vertex('sa', True, False)
    opt_graph.add_vertex('ta', False, True)
    # print(opt_graph.vertices)
    while True:
        # add vertices for graph level in use
        for nameIn in PKI_model.vertices:
            if PKI_model.vertices[nameIn]:
                opt_graph.add_vertex(nameIn)
                # print(nameIn)
        # add edges for the rooms in specific graph level
        # print(opt_graph.vertices)
        for key, value in PKI_model.edges.items():
            for v in value:
                # print(v)
                opt_graph.add_edge(key, v[0], v[1])

        # where we calculate our max flow
        flow_amount = opt_graph.calculate_max_flow()
        # if flow desired is found in current level of graph, we've found the graph to use
        if flow_amount == PKI_model.desired_flow:
            break
        # Else Add the second or third level of nodes and edges
        if level_count == 1:
            PKI_model.vertices.update(PKI_model.l2vertices)
            PKI_model.edges.update(PKI_model.l2edges)
        if level_count == 2:
            PKI_model.vertices.update(PKI_model.l3vertices)
            PKI_model.edges.update(PKI_model.l3edges)
        # if the desired flow cant be found, return an error
        if level_count == 3:
            break

        level_count = level_count + 1

    # Builds a network of only the edges with positive flow for usability in finding paths
    positive_flow_network = []
    for edge in opt_graph.get_edges():
        if edge.flow >= 0:
            positive_flow_network = positive_flow_network + [edge]
    path_a = find_path('s1', positive_flow_network, PKI_model.s1)
    path_b = find_path('s2', positive_flow_network, PKI_model.s2)
    path_c = find_path('s3', positive_flow_network, PKI_model.s3)
    all_paths = {'s1': path_a, 's2': path_b, 's3': path_c}
    return all_paths


