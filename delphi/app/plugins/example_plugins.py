"""
These plugins are both used as example plugins
to learn from as well as used in unit tests.
"""

from app import data_analyzer
from collections import namedtuple

class TestDataAnalyzerPlugin(data_analyzer.DataAnalyzerPlugin):
    IncrementData   = namedtuple('IncrementData', ('increment',))
    MaxConstraint   = namedtuple('MaxConstraint', ('max',))

    def __init__(self):
        super().__init__(TestDataAnalyzerPlugin.IncrementData._fields, TestDataAnalyzerPlugin.MaxConstraint._fields)

    def get_data_class(self):
        return TestDataAnalyzerPlugin.IncrementData
    
    def get_constraint_class(self):
        return TestDataAnalyzerPlugin.MaxConstraint
        
    def init(self):
        self.num = 0
        self.max = None

    def shutdown(self):
        self.num = -1

    def collect(self):
        return {'num': self.num}

    def analyze(self, data):
        self.num += data.increment
        if self.max is not None:
            self.num = min(self.num, self.max)

    def constraint(self, constraints):
        self.max = constraints.max
        self.num = min(self.num, self.max)

class TestDataAnalyzerPlugin2(data_analyzer.DataAnalyzerPlugin):
    NodeData            = namedtuple('NodeData', ('node_id', 'extra',), defaults=(None, None))
    MaxSizeConstraint   = namedtuple('MaxSizeConstraint', ('maxsize',))

    def __init__(self):
        super().__init__(TestDataAnalyzerPlugin2.NodeData._fields, TestDataAnalyzerPlugin2.MaxSizeConstraint._fields)

    def get_data_class(self):
        return TestDataAnalyzerPlugin2.NodeData
    
    def get_constraint_class(self):
        return TestDataAnalyzerPlugin2.MaxSizeConstraint
        
    def init(self):
        self.num      = 0
        self.nodes    = set()
        self.maxsize  = None

    def shutdown(self):
        self.nodes.clear()

    def collect(self):
        return {'nodes': list(self.nodes)}

    def analyze(self, data):
        if self.maxsize is not None and len(self.nodes) >= self.maxsize:
            return

        if data.node_id is not None:
            self.nodes.add(data.node_id)
            if data.extra is not None:
                self.num += data.extra

    def constraint(self, constraints):
        self.maxsize = constraints.maxsize