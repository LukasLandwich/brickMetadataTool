from neo4jConnector import Neo4JConnector
from ontologyResource import OntologyResource
from brickResource import BrickClassInstance, BrickPropertyInstance, BrickRelationshipInstance, BrickResource
from neo4j import Record
from resourceDictionary import ResourceDictionaty
from brickResourceType import BrickResourceType
from ontologyResource import OntologyResourceInstance

class MetadataAdapter():
    
    def __init__(self, db:Neo4JConnector, dictionary: ResourceDictionaty) -> None:
        self.db = db
        self.dict = dictionary
        
    
    def createNode(self, classisntance:BrickClassInstance, blueprint=False) -> bool:
        query = self.getCreationQuery(classisntance)
        if blueprint:
            result = self.db.executeQuery(query, Neo4JConnector.propertyStoreDatabasePath)
        else:
            result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        #TODO handle response and return fitting bool
        return True 
    
    def createRelationshipOnExisingNodes(self, relationshipInstance:BrickRelationshipInstance, fromInstance: BrickClassInstance, toInstance:BrickClassInstance) -> bool:
        query = """optional match(a) , (b) where Id(a) = {idFrom} and Id(b) = {idTo} create (a) -[c:{relType}]-> (b) return *""".format(idFrom = fromInstance.id, idTo = toInstance.id, relType = relationshipInstance.resource.name)
        self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return True
    
    def getEntityById(self, _id:int) -> BrickClassInstance:
        query = """MATCH (n) where ID(n) = {id} RETURN n""".format(id=_id)
        result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        classInstance = self.convertResultIntoClassInstance(result[0], "n")
        return classInstance
    
    def getClassOf(self, _id: int) -> BrickResource:
        classInstance = self.getEntityById(_id)
        return classInstance.resource
    
    def getBlueprintsOf(self, _class:str) -> [BrickClassInstance]:
        query = """Match (e:{className}) return e""".format(className=_class)
        result= self.db.executeQuery(query, Neo4JConnector.propertyStoreDatabasePath)
        return [self.convertResultIntoClassInstance(r, "e") for r in result]
    
    def getBlueprintById(self, _id:int) -> BrickClassInstance:
        query = """MATCH (n) where ID(n) = {id} RETURN n""".format(id=_id)
        result = self.db.executeQuery(query, Neo4JConnector.propertyStoreDatabasePath)
        blueprint = self.convertResultIntoClassInstance(result[0], "n")
        return blueprint
    
    
    def getAllExistingEntities(self) -> [BrickClassInstance]:
        query = "Match (e) return e"
        result= self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return [self.convertResultIntoClassInstance(r, "e") for r in result]   
    
    def getAllEntityClasses(self) -> [str]:
        query = "Match (e) with labels(e) as l return distinct l"
        result= self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        classes = [x["l"] for x in result]
        return classes
     
    def convertResultIntoClassInstance(self, record: Record, recordId:str) -> BrickClassInstance:
        node = record[recordId]
        keys = node.keys()
        id = node.id
        name = node['name']
        if len(node.labels) > 0:
            _classType, = node.labels
        else:
            return None
        properties = []
        for key in keys:
            if key == 'name':
                continue
            propertyValue = node[key]
            propertyResource = self.dict.getProperty(key)
            properties.append(BrickPropertyInstance(propertyResource,propertyValue))
        
        classResource = self.dict.getClass(_classType)
        classInstance = BrickClassInstance(classResource, name, properties, id)
        return classInstance
        #TODO Build for any kind of resource
    
    #------------Analytics Functions----------------
    
    def getTopNClasses(self, N) -> dict:
        query = """Match (e) with labels(e) as l, count(labels(e)) as cnt return l, cnt order by cnt desc Limit {limit}""".format(limit = N) 
        result= self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        if len(result) > 0:
            topNClasses = {r["l"][0]: {"count": r["cnt"], "description": self.dict.getClass(r["l"][0]).definition} for r in result} 
            return topNClasses
        else:
            return None

    
    def getNumberOfEntities(self) -> int:
        query = "MATCH (n) RETURN count(n) as cnt"
        result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return result[0]["cnt"]
    
    def getNumberOfRelationships(self) -> int:
        query = "MATCH ()-->() RETURN count(*) as cnt"
        result = self.db.executeQuery(query, Neo4JConnector.metadataDatabasePath)
        return result[0]["cnt"]
    
    def getMetadataStatistics(self):
        pass
    
    
     #---------------------Query Creators----------------------
    def getCreationQuery(self, instance: OntologyResourceInstance) -> str:
        if instance.resource.type == BrickResourceType.PROPERTY:
            return "{}: '{}'".format(instance.resource.name ,str(instance.value))
        elif instance.resource.type == BrickResourceType.CLASS:
            if len(instance.properties) == 0:
                propertyString = "{name: '" + instance.name + "'}"
            else:
                propertyString = "{name: '" + instance.name +"', " + ', '.join(self.getCreationQuery(p) for p in instance.properties) + "}"
            return "CREATE (:{} {})".format(instance.resource.name ,propertyString)
        elif instance.resource.type == BrickResourceType.RELATIONSHIP:
            pass
        else:
            print("Unknow Brick Resoruce Type. Please check and/or change implementaiton.")
            
    
    