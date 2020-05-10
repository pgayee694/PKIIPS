from delphi.app import data_analyzer
from collections import namedtuple

from delphi.app.graph import FlowNetwork
from delphi.app.pki_model import PKI


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


class GraphPlugin(data_analyzer.DataAnalyzerPlugin):
    RoomData = namedtuple('RoomData', ('Room', 'Count'))
    NodeConstraint = namedtuple('NodeConstraint', ('node_id',))

    def __init__(self):
        super().__init__(GraphPlugin.RoomData._fields, GraphPlugin.NodeConstraint._fields)

    def get_data_class(self):
        """
        returns Room Data class
        :return: room data class
        """
        return GraphPlugin.RoomData

    def get_constraint_class(self):
        """
        returns node constraint class
        :return: node constrain class
        """
        return GraphPlugin.NodeConstraint

    def init(self):
        """
        Initialization
        Attributes:
            pki: a PKI object for optimization
            routes: a dictionary of routes
        :return:
        """

        self.pki = PKI()
        self.routes = {}

    def shutdown(self):
        """
        shutdown
        :return:
        """
        self.pki = None

    def collect(self):
        """
        to collect routes
        :return: A dictionary of routes for each rooms
        """
        return {'paths': self.routes}

    def analyze(self, data):
        """
        Updates the people count in rooms and reruns the graph optimization
        :param data: room numbers with associated people counts
        :return:
        """
        self.pki.update_room(data.Room, data.Count)
        self.optimize()

    def constraint(self, constraints):
        """
        toggles the enabled/disabled statuses of nodes
        :param constraints: a list of node names passed in as strings
        :return:
        """
        self.pki.toggle(constraints.node_id)
        self.optimize()

    def optimize(self):
        """
        The main program which builds a network flow graph and then runs a network flow algorithm to insure all
        flow desired makes it through the network
        :return: n/a
        """
        # for iterating through while loop
        level_count = 1
        # create empty graph
        opt_graph = FlowNetwork()

        # add artificial source and sink and first level of vertices/edges
        opt_graph.add_vertex('sa', True, False)
        opt_graph.add_vertex('ta', False, True)
        for node in self.pki.vertex_levels['l1']:
            if self.pki.vertex_levels['l1'][node]:
                opt_graph.add_vertex(node)

        for key, value in self.pki.edge_levels['l1'].items():
            for v in value:
                opt_graph.add_edge(key, v[0], v[1])

        while True:
            # where we calculate our max flow
            flow_amount = opt_graph.calculate_max_flow()
            # if flow desired is found in current level of graph, we've found the graph to use
            if flow_amount == self.pki.desired_flow:
                break
            # Else Add the second or third level of nodes and edges
            if level_count == 1:
                for node in self.pki.vertex_levels['l2']:
                    if self.pki.vertex_levels['l2'][node]:
                        opt_graph.add_vertex(node)
                for key, value in self.pki.edge_levels['l2'].items():
                    for v in value:
                        opt_graph.add_edge(key, v[0], v[1])

            if level_count == 2:
                for node in self.pki.vertex_levels['l3']:
                    if self.pki.vertex_levels['l3'][node]:
                        opt_graph.add_vertex(node)
                for key, value in self.pki.edge_levels['l3'].items():
                    for v in value:
                        opt_graph.add_edge(key, v[0], v[1])

            # if the desired flow cant be found, return an error
            if level_count == 3:
                break

            level_count = level_count + 1

        # Builds a network of only the edges with positive flow for usability in finding paths
        positive_flow_network = []
        for edge in opt_graph.get_edges():
            if edge.flow >= 0:
                positive_flow_network = positive_flow_network + [edge]
        path_a = find_path('252', positive_flow_network, self.pki.room_counts['252'])
        path_b = find_path('256', positive_flow_network, self.pki.room_counts['256'])
        path_c = find_path('260', positive_flow_network, self.pki.room_counts['260'])
        self.routes = {'252': path_a, '256': path_b, '260': path_c}
