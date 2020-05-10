from collections import namedtuple
from collections import defaultdict

from app import data_analyzer
from app.pki_model import PKI

class StatusPlugin(data_analyzer.DataAnalyzerPlugin):
    StatusConstraint = namedtuple('StatusConstraint', ('node_id'))

    def __init__(self):
        super().__init__(None, StatusPlugin.StatusConstraint._fields)

    def get_constraint_class(self):
        return StatusPlugin.StatusConstraint

    def init(self):
        pki = PKI()
        self.statuses = defaultdict(lambda: True)

    def collect(self):
        return {'statuses': dict(self.statuses)}

    def constraint(self, constraints):
        self.statuses[constraints.node_id] = not self.statuses[constraints.node_id]