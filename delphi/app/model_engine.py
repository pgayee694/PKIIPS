import logging

"""
The model engine is where analyzers are stored for updating
and collecting data from.
"""

class ModelEngine(object):
    """
    Class for interfacing with many analyzers.
    """
    def __init__(self):
        """
        Constructor. Creates an empty list of analyzers.
        """
        self.analyzers = []
    
    def add_analyzer(self, analyzer):
        """
        Adds an analyzer to the list of managed analyzers.

        Parameters:
            analyzer (DataAnalyzerPlugin): An analyzer plugin
        """
        self.analyzers.append(analyzer)

    def update_data(self, data_payload):
        """
        Updates all the plugins with the given data payload.

        Parameters:
            data_payload (dictionary): A dictionary of key-value mappings
        """
        for analyzer in self.analyzers:
            specific_data = {keyword: data_payload[keyword] for keyword in analyzer.get_data_keywords() if keyword in data_payload}
            if len(specific_data) != 0:
                try:
                    analyzer.analyze(analyzer.get_data_class()(**specific_data))
                except Exception as e:
                    logging.warning(f"Exception thrown from sending data to '{analyzer.__name__}': {e}")

    def update_constraint(self, constraint_payload):
        """
        Updates all the plugins with the given constraint payload.

        Parameters:
            constraint_payload (dictionary): A dictionary of key-value mappings
        """
        for analyzer in self.analyzers:
            specific_data = {keyword: constraint_payload[keyword] for keyword in analyzer.get_constraint_keywords() if keyword in constraint_payload}
            if len(specific_data) != 0:
                analyzer.constraint(analyzer.get_constraint_class()(**specific_data))

    def collect(self):
        """
        Collects the current state of all the analyzers into one
        dictionary.

        Returns:
            (dictionary): The state of all analyzers updated by
                          calling the collect method on every
                          analyzer
        """
        data = {}

        for analyzer in self.analyzers:
            data.update(analyzer.collect())

        return data

    def start(self):
        """
        Starts up all the analyzers.
        """
        for analyzer in self.analyzers:
            analyzer.init()

    def stop(self):
        """
        Shuts down all the analyzers.
        """
        for analyzer in self.analyzers:
            analyzer.shutdown()