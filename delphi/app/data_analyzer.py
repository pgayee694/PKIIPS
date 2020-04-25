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
            (DataContainer): A map of keywords to values.
        """
        pass

    def analyze(self, data):
        """
        Called whenever new data has been recieved to analyze. Will only be called
        if the data payload contains the required keywords that this analyzer is
        listening for. Will also only get the data payload containing the keywords
        that this analyzer is listening for.

        Parameters:
            data (DataContainer): A map of keywords to values.
        """
        pass

    def constraint(self, constraints):
        """
        Called whenever a new constraint has been recieved. Will only be called
        if the constraint payload contains the required keywords that this analyzer is
        listening for.

        Parameters:
            constraints (ConstraintsContainer): A map of keywords to values.
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

class DataContainer(object):
    """
    A wrapper class around a dictionary to indicate a data payload.
    """
    def __init__(self, data_dict):
        """
        Initializes this object with the given dictionary.

        Parameters:
            data_dict (dict): Data payload
        """
        self.data = data_dict
    
    def get(self, keyword):
        """
        Retrieves the data associated with the given keyword, or None
        if it does not exist.

        Parameters:
            keyword (string): A keyword

        Returns:
            (object or None): Returns an object is one has an associated
                              keyword, otherwise returns None
        """
        return self.data.get(keyword, None)
    
    def __getitem__(self, key):
        """
        Retrieves the data associated with the given keyword, or None
        if it does not exist.

        Parameters:
            key (string): A keyword

        Returns:
            (object or None): Returns an object is one has an associated
                              keyword, otherwise returns None
        """
        return self.get(key)

    def keywords(self):
        """
        Gets all the keywords of this data payload.

        Returns:
            (set [string]): A set of keywords
        """
        return self.data.keys()

    def contains_keyword(self, keyword):
        """
        Checks if this data payload contains the given keyword.

        Parameters:
            keyword (string): keyword to check

        Returns:
            (bool): True if the given keyword is in this data container,
                    False otherwise
        """
        return keyword in self.data
    
    def __iter__(self):
        """
        Returns an iterator over the internal dictionary.
        """
        return iter(self.data)

class ConstraintsContainer(object):
    """
    A wrapper class around a dictionary to indicate a constraints payload.
    """
    def __init__(self, data_dict):
        """
        Initializes this object with the given dictionary.

        Parameters:
            data_dict (dict): Constraints payload
        """
        self.data = data_dict
    
    def get(self, keyword):
        """
        Retrieves the constraint associated with the given keyword, or None
        if it does not exist.

        Parameters:
            keyword (string): A keyword

        Returns:
            (object or None): Returns an object is one has an associated
                              keyword, otherwise returns None
        """
        return self.data.get(keyword, None)
    
    def __getitem__(self, key):
        """
        Retrieves the constraint associated with the given keyword, or None
        if it does not exist.

        Parameters:
            key (string): A keyword

        Returns:
            (object or None): Returns an object is one has an associated
                              keyword, otherwise returns None
        """
        return self.get(key)

    def keywords(self):
        """
        Gets all the keywords of this constraints payload.

        Returns:
            (set [string]): A set of keywords
        """
        return self.data.keys()

    def contains_keyword(self, keyword):
        """
        Checks if this constraints payload contains the given keyword.

        Parameters:
            keyword (string): keyword to check

        Returns:
            (bool): True if the given keyword is in this constraints container,
                    False otherwise
        """
        return keyword in self.data
    
    def __iter__(self):
        """
        Returns an iterator over the internal dictionary.
        """
        return iter(self.data)