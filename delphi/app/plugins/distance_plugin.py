from app import data_analyzer
from collections import namedtuple
from app import global_model_engine

class DistanceAnalyzerPlugin(data_analyzer.DataAnalyzerPlugin):
    """
    Filters the count of people based off of the distance to them to avoid
    overcounting
    """

    class PeopleCount():

        def __init__(self, id_, room, range_, count, distances):
            self.id_ = id_
            self.room = room
            self.range_ = range_
            self.count = count
            self.distances = distances

    def __init__(self):
        super().__init__(['id', 'room', 'range', 'count', 'distances'], None)
    
    def get_data_class(self):
        return DistanceAnalyzerPlugin.PeopleCount
    
    def get_constraint_class(self):
        pass
    
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

        for seer in self.seers:
            if seer.room in data.keys():
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
            if seer.room == seerCount.room and seer.id_ == seerCount.id_:
                # update an existing entry
                newCount = seerCount.count

                for d in seerCount.distances:
                    if d > seerCount.range_:
                        newCount -= 1

                seer.count = newCount
                break
            elif seer.room == seerCount.room:
                # we have multiple seers in the same room, so process the "old's" counts to be within range
                roomExists = True
                for d in seer.distances:
                    if d > seer.range_:
                        seer.count -= 1
        else:
            # new seer
            if roomExists:
                # new node in the same room as another
                for d in seerCount.distances:
                    if d > seerCount.range_:
                        seerCount.count -= 1

            self.seers.append(seerCount)
        
        count = 0
        for seer in self.seers:
            if seer.room == seerCount.room:
                count += seer.count
        
        propagate = {
            'Room': seerCount.room,
            'Count': count
        }

        # update the model engine with the newly processed data
        global_model_engine.update_data(propagate)
    
    def constraint(self):
        pass
