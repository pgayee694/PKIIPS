from delphi.app import data_analyzer
from collections import namedtuple

from delphi.app.pki_model import PKI


class GraphPlugin(data_analyzer.DataAnalyzerPlugin):
    RoomData = namedtuple('RoomData', ('Room#', 'Count'))
    NodeConstraint = namedtuple('NodeConstraint', ('node',))

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
        return self.routes

    def analyze(self, data):
        """
        Updates the people count in rooms and reruns the graph optimization
        :param data: room numbers with associated people counts
        :return:
        """
        for room in data:
            self.pki.update_room(room[0], room[1])
        self.routes = self.pki.run()

    def constraint(self, constraints):
        """
        toggles the enabled/disabled statuses of nodes
        :param constraints: a list of node names passed in as strings
        :return:
        """
        for node in constraints:
            self.pki.toggle(node)
