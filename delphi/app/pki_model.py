from delphi.app.graph import run_optimization


class PKI:
    """
    PKI is a class to represent the building PKI.

    Attributes:
        vertices: a dictionary of nodes and their enabled status
        l2vertices: a dictionary of nodes and their enabled status
        l3vertices: a dictionary of nodes and their enabled status
        s1: the people count of room s1
        s2: the people count of room s2
        s3: the people count of room s3
        desired_flow: the amount of people that need to exit pki
        edges: a dictionary of edges and their weights
        l2edges: a dictionary of edges and their weights
        l3edges: a dictionary of edges and their weights
    """

    def __init__(self):
        """
        PKI constructor
        """
        self.vertices = {'t1': True, 't2': True, 's1': True, 's2': True, 's3': True, 'h1': True, 'h2': True, 'h5': True}
        self.l2vertices = {'t3': True, 't4': True, 'h3': True, 'h4': True}
        self.l3vertices = {'h6': True}
        self.s1 = 25
        self.s2 = 30
        self.s3 = 20
        self.setEdges()
        self.desired_flow = self.s1 + self.s2 + self.s3

    def toggle(self, node):
        """
        This method is designed to toggle the enabled status of the node passed in
        :param node: the name of the ndoe to toggle
        :return: n/a
        """
        if node in self.vertices:
            for key in self.vertices:
                if node == key:
                    if self.vertices[key] is True:
                        new = {key: False}
                        self.vertices.update(new)
                    else:
                        new = {key: True}
                        self.vertices.update(new)
        elif node in self.l2vertices:
            for key in self.l2vertices:
                if node == key:
                    if self.l2vertices[key] is True:
                        new = {key: False}
                        self.l2vertices.update(new)
                    else:
                        new = {key: True}
                        self.l2vertices.update(new)
        else:
            for key in self.l3vertices:
                if node == key:
                    if self.l3vertices[key] is True:
                        new = {key: False}
                        self.l3vertices.update(new)
                    else:
                        new = {key: True}
                        self.l3vertices.update(new)

    def update_room(self, node, new_count):
        """
        this method updates the people count of a room
        :param node: the name of the room to update
        :param new_count: the new people count for that room
        :return: n/a
        """
        if node == 's1':
            self.s1 = new_count
        elif node == 's2':
            self.s2 = new_count
        elif node == 's3':
            self.s3 = new_count

        self.desired_flow = self.s1 + self.s2 + self.s3
        self.setEdges()

    def setEdges(self):
        """
        This method sets the values of the edges. It is accessed when PKI is initialized and
        when it is updated
        :return: n/a
        """
        self.edges = {"sa": [("s1", 1000), ("s2", 1000), ('s3', 1000)], "s1": [("h1", self.s1)],
                      "s2": [("h1", self.s2)], "s3": [("h1", self.s3)], "h1": [("h2", 80)],
                      "h2": [("h5", 75), ("t1", 25)], "t1": [("ta", 1000)], "t2": [("ta", 1000)], "h5": [("t2", 80)]}
        self.l2edges = {"s1": [("h1", self.s1 / 2), ("h3", self.s1 / 2)], "h3": [("h4", 1)],
                        "h4": [("t3", 1), ("t4", 1)], "t3": [("ta", 1000)],
                        "t4": [("ta", 1)]}
        self.l3edges = {"s3": [("h1", self.s3 / 2), ("h6", self.s3 / 2)], "h6": [("h4", 1)]}

    def run(self):
        """
        This method runs optimization of PKI
        :return: n/a
        """
        run_optimization(self)


