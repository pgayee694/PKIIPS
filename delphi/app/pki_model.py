from delphi.app.graph import run_optimization


class PKI:
    def __init__(self):
        self.vertices = {'t1': True, 't2': True, 's1': True, 's2': True, 's3': True, 'h1': True, 'h2': True, 'h5': True}
        self.l2vertices = {'t3': True, 't4': True, 'h3': True, 'h4': True}
        self.l3vertices = {'h6': True}
        self.s1 = 25
        self.s2 = 30
        self.s3 = 20
        self.edges = {"sa": [("s1", 1000), ("s2", 1000), ('s3', 1000)], "s1": [("h1", self.s1)],
                      "s2": [("h1", self.s2)], "s3": [("h1", self.s3)], "h1": [("h2", 80)],
                      "h2": [("h5", 75), ("t1", 25)], "t1": [("ta", 1000)], "t2": [("ta", 1000)], "h5": [("t2", 80)]}
        self.l2edges = {"s1": [("h1", self.s1 / 2), ("h3", self.s1 / 2)], "h3": [("h4", 1)],
                        "h4": [("t3", 1), ("t4", 1)], "t3": [("ta", 1000)],
                        "t4": [("ta", 1)]}
        self.l3edges = {"s3": [("h1", self.s3 / 2), ("h6", self.s3 / 2)], "h6": [("h4", 1)]}
        self.desired_flow = 75
        self.count_data = self.s1 + self.s2 + self.s3

    def toggle(self, node):
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

    def update_room(self, node, count):
        if node == 's1':
            self.s1 = count
        elif node == 's2':
            self.s2 = count
        elif node == 's3':
            self.s3 = count
        if node in self.l2edges:
            for key in self.l2edges:
                if key == node:
                    for v in self.l2edges[key]:
                        print(v)
        # if node in self.l2edges:
        # if node in self.l3edges:

    def run(self):
        run_optimization(self)


testpki = PKI()
testpki.run()
testpki.update_room('s1', 8)
testpki.run()