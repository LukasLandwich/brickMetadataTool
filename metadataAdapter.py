from neo4jConnector import Neo4JConnector
from ontologyResource import OntologyResource

class MetadataAdapter():
    
    def __init__(self, db:Neo4JConnector) -> None:
        self.db = db
        
        
    #------------Analytics Functions----------------
    
    def getTopNClasses(self, N) -> dict:
        query = """Match (e) with labels(e) as l, count(labels(e)) as cnt return l, cnt order by cnt desc Limit {limit}""".format(limit = N) 
        result= self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        
        topNClasses = dict(map(lambda n: (n["l"][0], n["cnt"]), result))
        print(topNClasses)
        return topNClasses
    
    def getNumberOfEntities(self) -> int:
        query = "MATCH (n) RETURN count(n) as cnt"
        result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return result[0]["cnt"]
    
    def getNumberOfRelationships(self) -> int:
        query = "MATCH ()-->() RETURN count(*) as cnt"
        result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return result[0]["cnt"]
    
    def getAllClassesOf(self, resource:OntologyResource):
        query = """Match (c:{lable}) return c""".format(resource.lable)
    
    def getMetadataStatistics(self):
        pass