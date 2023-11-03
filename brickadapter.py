import brickschema
from brickResource import BrickClass, BrickProperty, BrickRelationship
class BrickAdapter:
   
    
    def __init__(self, db) -> None:
        self.db = db
        
        if not db.hasBrickInitialized():
            print("Brick Onntology isnt initilaized.")
            db.loadBrickOntology()
  
    def getAllClasses(self) -> [BrickClass]:
        classes, summary, keys = self.db.driver.execute_query(
        "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_="brickSchema",
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickClass(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return classesList
    
  
    def getAllRelationships(self) -> [BrickRelationship]:
       

        relationships, summary, keys = self.db.driver.execute_query(
        "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_="brickSchema",
        )   
        relationshipsList = []
        for resource in relationships:
            relationshipsList.append(BrickRelationship(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return relationshipsList
    
    def getAllProperties(self) -> [BrickProperty]:
        properties, summary, keys = self.db.driver.execute_query(
        "MATCH (a:Resource) WHERE SIZE(LABELS(a)) = 1 RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__defintion as defintion, a.uri as uri",
        database_="brickSchema",
        )   
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"], resource["label"], resource["defintion"], resource["uri"]))
            
        return propertiesList
    
    def getPropertiesOf(self, _class) -> [BrickProperty]:
        query =  """MATCH (b)-[:n4sch__SCO*0..5]->(a:n4sch__Class) <-[:n4sch__DOMAIN]-(p) where a.n4sch__name='{className}' OR b.n4sch__name='{className}' RETURN p.n4sch__name as name, p.n4sch__label as label, p.n4sch__defintion as defintion, p.uri as uri""".format(className = _class)
        print(query)
        properties, summary, keys = self.db.driver.execute_query(query,
            database_="brickSchema")
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"] , resource["label"], resource["defintion"], resource["uri"]))
        return propertiesList
        
        
    def getRelationshipsOf(self, _class) -> [BrickRelationship]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = "Fluid"  Return pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__defintion as defintion, pcrel.uri as uri""".format(className = _class)
        relationships, summary, keys = self.db.driver.execute_query(query,
            database_="brickSchema")
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickRelationship(resource["name"] , resource["label"], resource["defintion"], resource["uri"]))
        return relationshipList