import re
import datetime

class Ranking:
    def __init__(self, rank, name, id, power, kingdom):
        self.rank = rank
        self.id = id
        self.power = power
        self.date = datetime.datetime.now()
        self.kingdom = kingdom

        match = re.match(r'^(\[([^\]]+)\])?(.*)', name)

        if match:
            self.alliance = match.group(2)
            self.name = match.group(3)
        else:
            self.alliance = None
            self.name = name
    
    def __repr__(self):
        return f'{self.name} ({self.id}): #{self.rank}, {self.power}'
