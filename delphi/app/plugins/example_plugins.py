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