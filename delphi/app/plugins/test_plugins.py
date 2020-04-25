"""
These plugins are both used as example plugins
to learn from as well as used in unit tests.
"""

from app import data_analyzer

class TestDataAnalyzerPlugin(data_analyzer.DataAnalyzerPlugin):
    increment_keyword   = 'increment'
    max_keyword         = 'max'
    data_keywords       = (increment_keyword,)
    constraint_keywords = (max_keyword,)

    def __init__(self):
        super().__init__(TestDataAnalyzerPlugin.data_keywords, TestDataAnalyzerPlugin.constraint_keywords)        
        
    def init(self):
        self.num = 0
        self.max = None

    def shutdown(self):
        self.num = -1

    def collect(self):
        return data_analyzer.DataContainer({'num': self.num})

    def analyze(self, data):
        if data.contains_keyword(TestDataAnalyzerPlugin.increment_keyword):
            self.num += data[TestDataAnalyzerPlugin.increment_keyword]
            if self.max is not None:
                self.num = min(self.num, self.max)

    def constraint(self, constraints):
        if constraints.contains_keyword(TestDataAnalyzerPlugin.max_keyword):
            self.max = constraints[TestDataAnalyzerPlugin.max_keyword]
            self.num = min(self.num, self.max)