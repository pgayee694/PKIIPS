class DataAnalyzerPlugin(object):
    """
    All Data Analyzer plugins should inherit from this class.
    """
    def __init__(self, data_keywords=None, constraint_keywords=None):
        """
        Initializes what keywords this analyzer is listening for.

        Parameters:
            data_keywords (Iterable): An object that is iterable
            constraint_keywords (Iterable): An object that is iterable
        """
        self.data_keywords          = set() if data_keywords is None else set(data_keywords)
        self.constraint_keywords    = set() if constraint_keywords is None else set(constraint_keywords)

    def get_data_class(self):
        """
        Returns a class type that will be constructed and passed to the analyze function
        upon a data payload. This class must take in keyword arguments in its constructor
        to initialize its fields.

        Returns:
            (type): a class type
        """
        pass

    def get_constraint_class(self):
        """
        Returns a class type that will be constructed and passed to the constraint function
        upon a constraint payload. This class must take in keyword arguments in its constructor
        to initialize its fields.

        Returns:
            (type): a class type
        """
        pass

    def init(self):
        """
        Called once before the plugin has recieved any data. Meant to
        initialize any resources before analyzing.
        """
        pass

    def shutdown(self):
        """
        Called when the delphi server shutsdown. Meant to clean up
        any resources that this plugin uses.
        """
        pass

    def collect(self):
        """
        Called whenever the current state of this data analyzer is needed.
        
        Returns:
            (dictionary): A map of keywords to values.
        """
        pass

    def analyze(self, data):
        """
        Called whenever new data has been recieved to analyze. Will only be called
        if the data payload contains the required keywords that this analyzer is
        listening for. Will also only get the data payload containing the keywords
        that this analyzer is listening for.

        Parameters:
            data (object): A custom object that is defined by the type returned
                           by get_data_class
        """
        pass

    def constraint(self, constraints):
        """
        Called whenever a new constraint has been recieved. Will only be called
        if the constraint payload contains the required keywords that this analyzer is
        listening for.

        Parameters:
            constraints (object): A custom object that is defined by the type returned
                                  by get_constraint_class
        """
        pass

    def get_data_keywords(self):
        """
        Gets all the data keywords this plugin is listening to.

        Returns:
            (set[string]): keywords
        """
        return self.data_keywords

    def get_constraint_keywords(self):
        """
        Gets all the constraint keywords this plugin is listening to.

        Returns:
            (set[string]): keywords
        """
        return self.constraint_keywords

    def has_data_keyword(self, keyword):
        """
        Check if this plugin is listening to the given keyword in data
        payloads.

        Parameters:
            keyword (string): A keyword

        Returns:
            (bool): True if the keyword is being listened to in data
                    payloads, false otherwise
        """
        return keyword in self.data_keywords

    def has_constraint_keyword(self, keyword):
        """
        Check if this plugin is listening to the given keyword in constraint
        payloads.

        Parameters:
            keyword (string): A keyword

        Returns:
            (bool): True if the keyword is being listened to in constraint
                    payloads, false otherwise
        """
        return keyword in self.constraint_keywords