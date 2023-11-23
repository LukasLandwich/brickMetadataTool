import brickschema
from brickResource import BrickClass, BrickProperty, BrickRelationship, BrickClassInstance
from neo4jConnector import Neo4JConnector
class BrickAdapter:
   
    brickDatabasePath = "brickSchema"
    metadataDatabasePath = "metadata"
    propertyStoreDatabasePath = "propertystore"
    
    def __init__(self, db:Neo4JConnector) -> None:
        self.db = db
        
        if not db.hasBrickInitialized():
            print("Brick Onntology isnt initilaized.")
            db.loadBrickOntology()
  
    def getAllClasses(self) -> [BrickClass]:
        classes = self.db.executeQuery(
        "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        self.brickDatabasePath,
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickClass(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return classesList
    
  
    def getAllRelationships(self) -> [BrickRelationship]:
       

        relationships = self.db.executeQuery(
        "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        self.brickDatabasePath,
        )   
        relationshipsList = []
        for resource in relationships:
            relationshipsList.append(BrickRelationship(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return relationshipsList
    
    def getAllProperties(self) -> [BrickProperty]:
        properties = self.db.executeQuery(
        "MATCH (a:Resource) WHERE SIZE(LABELS(a)) = 1 RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        self.brickDatabasePath,
        )   
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return propertiesList
    
    def getPropertiesOf(self, _class) -> [BrickProperty]:  
        query =  """MATCH (p)- [:n4sch__DOMAIN] ->(b)<-[:n4sch__SCO*0..5]-(a:n4sch__Class) where not p:n4sch__Relationship and a.n4sch__name='{className}' RETURN Distinct p.n4sch__name as name, p.n4sch__label as label, p.n4sch__definition as definition, p.uri as uri""".format(className = _class)
        print(query)
        properties = self.db.executeQuery(query, self.brickDatabasePath)
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"] , resource["label"], resource["definition"], resource["uri"]))
        return propertiesList
    
    def getDescriptionOf(self, _class) -> [BrickProperty]:  
        query =  """MATCH (a:n4sch__Class) where a.n4sch__name='{className}' RETURN a.n4sch__definition as definition""".format(className = _class)
        result = self.db.executeQuery(query, self.brickDatabasePath)
        if len(result) == 0:
            description = "No description available."
        else:
            description = result[0]["definition"]
        
        return description
        
        
    def getRelationshipsOf(self, _class) -> [BrickRelationship]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = '{className}'  Return Distinct pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__definition as definition, pcrel.uri as uri""".format(className = _class)
        relationships = self.db.executeQuery(query, self.brickDatabasePath)
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickRelationship(resource["name"] , resource["label"], resource["definition"], resource["uri"]))
        return relationshipList
    
    def getClassResource(self, name:str) -> BrickClass:
        query = """match (c:n4sch__Class) where c.n4sch__label = '{className}' Return c.n4sch__name as name, c.n4sch__label as label, c.n4sch__defintion as definition, c.uri as uri""".format(className = name) 
        brickClass = self.db.executeQuery(query, self.brickDatabasePath)
        resource = brickClass[0]
        return BrickClass(resource["name"] , resource["label"], resource["definition"], resource["uri"])
    
    def createNode(self, classisntance:BrickClassInstance, database) -> bool:
        query = classisntance.getCreationQuery()
        relationships = self.db.executeQuery(query,database)
        #TODO handle response and return fitting bool
        return True
        
    
    
    #def createRelationship(self, type:str,)
    
    
    
    #------------Analytics Functions----------------
    
    def getTopNClasses(self, N) -> dict:
        query = """Match (e) with labels(e) as l, count(labels(e)) as cnt return l, cnt order by cnt desc Limit {limit}""".format(limit = N) 
        result= self.db.executeQuery(query, self.metadataDatabasePath)
        
        topNClasses = dict(map(lambda n: (n["l"][0], n["cnt"]), result))
        print(topNClasses)
        return topNClasses
    
    def getNumberOfEntities(self) -> int:
        query = "MATCH (n) RETURN count(n) as cnt"
        result = self.db.executeQuery(query, self.metadataDatabasePath)
        return result[0]["cnt"]
    
    def getNumberOfRelationships(self) -> int:
        query = "MATCH ()-->() RETURN count(*) as cnt"
        result = self.db.executeQuery(query, self.metadataDatabasePath)
        return result[0]["cnt"]
    
    
    def getMetadataStatistics(self):
        pass