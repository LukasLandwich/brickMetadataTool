import brickschema
from brickResource import BrickClass, BrickProperty, BrickRelationship, BrickClassInstance
class BrickAdapter:
   
    brickDatabasePath="brickSchema"
    metadataDatabasePath ="metadata"
    
    def __init__(self, db) -> None:
        self.db = db
        
        if not db.hasBrickInitialized():
            print("Brick Onntology isnt initilaized.")
            db.loadBrickOntology()
  
    def getAllClasses(self) -> [BrickClass]:
        classes, summary, keys = self.db.driver.execute_query(
        "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_= self.brickDatabasePath,
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickClass(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return classesList
    
  
    def getAllRelationships(self) -> [BrickRelationship]:
       

        relationships, summary, keys = self.db.driver.execute_query(
        "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_=self.brickDatabasePath,
        )   
        relationshipsList = []
        for resource in relationships:
            relationshipsList.append(BrickRelationship(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return relationshipsList
    
    def getAllProperties(self) -> [BrickProperty]:
        properties, summary, keys = self.db.driver.execute_query(
        "MATCH (a:Resource) WHERE SIZE(LABELS(a)) = 1 RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_= self.brickDatabasePath,
        )   
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return propertiesList
    
    def getPropertiesOf(self, _class) -> [BrickProperty]:  
        query =  """MATCH (p)- [:n4sch__DOMAIN] ->(b)<-[:n4sch__SCO*0..5]-(a:n4sch__Class) where a.n4sch__name='{className}' RETURN Distinct p.n4sch__name as name, p.n4sch__label as label, p.n4sch__definition as defintion, p.uri as uri""".format(className = _class)
        print(query)
        properties, summary, keys = self.db.driver.execute_query(query,
            database_= self.brickDatabasePath)
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"] , resource["label"], resource["defintion"], resource["uri"]))
        return propertiesList
        
        
    def getRelationshipsOf(self, _class) -> [BrickRelationship]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = '{className}'  Return Distinct pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__defintion as defintion, pcrel.uri as uri""".format(className = _class)
        relationships, summary, keys = self.db.driver.execute_query(query,
            database_= self.brickDatabasePath)
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickRelationship(resource["name"] , resource["label"], resource["defintion"], resource["uri"]))
        return relationshipList
    
    def getClassResource(self, name:str) -> BrickClass:
        query = """match (c:n4sch__Class) where c.n4sch__label = '{className}' Return c.n4sch__name as name, c.n4sch__label as label, c.n4sch__defintion as defintion, c.uri as uri""".format(className = name) 
        brickClass, summary, keys = self.db.driver.execute_query(query,
            database_= self.brickDatabasePath)
        resource = brickClass[0]
        return BrickClass(resource["name"] , resource["label"], resource["defintion"], resource["uri"])
    
    def createNode(self, classisntance:BrickClassInstance) -> bool:
        relationships, summary, keys = self.db.driver.execute_query(classisntance.getCreationQuery(),
            database_= self.metadataDatabasePath)
        #TODO handle response and return fitting bool
        return True
        
    def createNode(self, name:str, label:str, properties:dict) -> bool:
        relationships, summary, keys = self.db.driver.execute_query(BrickClassInstance.getCreationQuery(name, label, properties),
            database_= self.metadataDatabasePath)
        #TODO handle response and return fitting bool
        return True
    
    def getTopNClasses(self, N) -> dict:
        query = """Match (e) with labels(e) as l, count(labels(e)) as cnt return l, cnt order by cnt desc Limit {limit}""".format(limit = N) 
        topNClasses, summary, keys = self.db.driver.execute_query(query,
            database_= self.metadataDatabasePath)
        return topNClasses
    
    def getNumberOfEntities(self) -> int:
        query = "MATCH (n) RETURN count(n) as cnt"
        result, summary, keys = self.db.driver.execute_query(query,
            database_= self.metadataDatabasePath)
        return result["cnt"]
    
    def getNumberOfRelationships(self) -> int:
        query = "MATCH ()-->() RETURN count(*) as cnt"
        result, summary, keys = self.db.driver.execute_query(query,
            database_= self.metadataDatabasePath)
        return result["cnt"]
    
    
    def getMetadataStatistics(self):
        pass