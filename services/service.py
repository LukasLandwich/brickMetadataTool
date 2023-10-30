from neo4jConnector import Neo4JConnector
class Service:
    def __init__(self, db:Neo4JConnector, name):
        self.db = db
        self.name = name
        pass
    
    def checkForRecommendation(self):
        if self.db == None:
            return False
        