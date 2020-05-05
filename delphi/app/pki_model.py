from delphi.app.graph import run_optimization


class PKI:
    """
    PKI is a class to represent the building PKI.

    Attributes:
        vertex_levels: a dictionary of dictionaries of nodes and their status
        edge_levels: a dictionary of dictionaries of edges and their weights
        room_counts: a dictionary of rooms and their people counts
        desired_flow: the desired flow for the flow network
    """

    def __init__(self):
        """
        PKI constructor
        """
        self.setVertices()
        self.room_counts = {'s1': 25, 's2': 30, 's3': 20}
        self.setDesiredFlow()
        self.setEdges()

    def toggle(self, node_to_toggle):
        """
        This method is designed to toggle the enabled status of the node passed in
        :param node_to_toggle: the name of the node to toggle
        :return: the changed node and new status
        """
        new = {}
        for level in self.vertex_levels.values():
            for key in level:
                if node_to_toggle == key:
                    if level[key] is True:
                        new = {key: False}
                        level.update(new)
                    else:
                        new = {key: True}
                        level.update(new)

        return new

    def update_room(self, node, new_count):
        """
        this method updates the people count of a room
        :param node: the name of the room to update
        :param new_count: the new people count for that room
        """
        if node == 's1':
            self.room_counts['s1'] = new_count
        elif node == 's2':
            self.room_counts['s2'] = new_count
        elif node == 's3':
            self.room_counts['s3'] = new_count

        self.setDesiredFlow()
        self.setEdges()

    def setEdges(self):
        """
        This method sets the values of the edges. It is accessed when PKI is initialized and
        when it is updated
        """
        self.edge_levels = {
            "l1": {"sa": [("s1", 1000), ("s2", 1000), ('s3', 1000)], "s1": [("h1", self.room_counts['s1'])],
                   "s2": [("h1", self.room_counts['s2'])], "s3": [("h1", self.room_counts['s3'])], "h1": [("h2", 80)],
                   "h2": [("h5", 75), ("t1", 25)], "t1": [("ta", 1000)], "t2": [("ta", 1000)], "h5": [("t2", 80)]},
            "l2": {"s1": [("h1", self.room_counts['s1'] / 2), ("h3", self.room_counts['s1'] / 2)], "h3": [("h4", 1)],
                   "h4": [("t3", 1), ("t4", 1)], "t3": [("ta", 1000)],
                   "t4": [("ta", 1)]},
            'l3': {"s3": [("h1", self.room_counts['s3'] / 2), ("h6", self.room_counts['s3'] / 2)], "h6": [("h4", 1)]}}

    def setVertices(self):
        """
        A set function for the vertex dictionary
        """
        self.vertex_levels = {
            'l1': {'t1': True, 't2': True, 's1': True, 's2': True, 's3': True, 'h1': True, 'h2': True, 'h5': True},
            'l2': {'t3': True, 't4': True, 'h3': True, 'h4': True}, 'l3': {'h6': True}}

    def setDesiredFlow(self):
        """
        A set function for the desired flow
        """
        self.desired_flow = self.room_counts['s1'] + self.room_counts['s2'] + self.room_counts['s3']

    def run(self):
        """
        This method runs optimization of PKI
        :return: list of paths
        """
        return run_optimization(self)
