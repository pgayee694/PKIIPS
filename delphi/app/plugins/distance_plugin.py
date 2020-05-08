from app import data_analyzer
from collections import namedtuple
from app import global_model_engine

class DistanceAnalyzerPlugin(data_analyzer.DataAnalyzerPlugin):
    """
    Filters the count of people based off of the distance to them to avoid
    overcounting
    """

    PeopleCount = namedtuple('PeopleCount', ('id', 'room', 'range', 'count', 'distances'))

    def __init__(self):
        super().__init__(DistanceAnalyzerPlugin.SeerCount._fields, None)
    
    def get_data_class(self):
        return DistanceAnalyzerPlugin.SeerCount
    
    def get_constraint_class(self):
        return None
    
    def init(self):
        """
        Initializes the list of seers to keep data from each node
        """

        self.seers = []
    
    def shutdown(self):
        self.seers = None

    def collect(self):
        """
        Aggregates the counts for each room into a map of the room to the count

        :return: map of counts
        """

        data = {}

        for seer in seers:
            if data[seer.room]:
                data[seer.room] += seer.count
            else:
                data[seer.room] = seer.count
        
        return {
            'Counts' : data
        }

    def analyze(self, seerCount):
        """
        Update the count on the seer node in the list if it exists,
        otherwise add a new entry to the list. THen, propagate the
        filtered data out to all other analyzers
        """

        roomExists = False

        for seer in self.seers:
            if seer.room == seerCount.room and seer.id == seerCount.id:
                # update an existing entry
                newCount = seerCount.count

                for d in seerCount.distances:
                    if d > seerCount.range:
                        newCount -= 1

                seer.count = newCount
                break
            elif seer.room == seerCount.room:
                roomExists = True
        else:
            if roomExists:
                for d in seerCount.distances:
                    if d > seerCount.range:
                        seerCount -= 1

            self.seers.append(seerCount)
        
        count = 0
        for seer in self.seers:
            if seer.room == seerCount.room:
                count += seer.count
        
        propagate = {
            'Room': seerCount.room
            'Count': count
        }

        # update the model engine with the newly processed data
        global_model_engine.update_data(propagate)
