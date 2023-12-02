from brickResource import BrickClass, BrickProperty, BrickRelationship, BrickClassInstance
from neo4jConnector import Neo4JConnector
from OntologyAdapter import OntologyAdapter
class BrickAdapter(OntologyAdapter):
       
    brickSchemaDownloadPath = "'https://brickschema.org/schema/1.3.0/Brick.ttl'"
    brickSchemaDownloadFileType = "'Turtle'"
    
    def __init__(self, db:Neo4JConnector) -> None:
        self.db = db
        
        if not self.isOntologyInitialized():
            print("Brick Onntology isnt initilaized.")
            self.loadOntology()
  
    def getAllClasses(self) -> [BrickClass]:
        classes = self.db.executeQuery(
        "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickClass(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return classesList
    
  
    def getAllRelationships(self) -> [BrickRelationship]:
       

        relationships = self.db.executeQuery(
        "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        relationshipsList = []
        for resource in relationships:
            relationshipsList.append(BrickRelationship(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return relationshipsList
    
    def getAllProperties(self) -> [BrickProperty]:
        properties = self.db.executeQuery(
        "MATCH (a:Resource) WHERE SIZE(LABELS(a)) = 1 RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"], resource["label"], resource["definition"], resource["uri"]))
            
        return propertiesList
    
    def getPossiblePropertiesOf(self, _class:str) -> [BrickProperty]:  
        query =  """MATCH (p)- [:n4sch__DOMAIN] ->(b)<-[:n4sch__SCO*0..5]-(a:n4sch__Class) where not p:n4sch__Relationship and a.n4sch__name='{className}' RETURN Distinct p.n4sch__name as name, p.n4sch__label as label, p.n4sch__definition as definition, p.uri as uri""".format(className = _class)
        print(query)
        properties = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickProperty(resource["name"] , resource["label"], resource["definition"], resource["uri"]))
        return propertiesList      
        
    def getPossibleRelationshipsOf(self, _class:str) -> [BrickRelationship]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = '{className}'  Return Distinct pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__definition as definition, pcrel.uri as uri""".format(className = _class)
        relationships = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickRelationship(resource["name"] , resource["label"], resource["definition"], resource["uri"]))
        return relationshipList
    
    def getClass(self, name:str) -> BrickClass:
        query = """match (c:n4sch__Class) where c.n4sch__label = '{className}' Return c.n4sch__name as name, c.n4sch__label as label, c.n4sch__defintion as definition, c.uri as uri""".format(className = name) 
        brickClass = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
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
    
    
    def getMetadataStatistics(self):
        pass
    
    
    
    
    #--------------------Ontology Management-----------------
    
    def isOntologyInitialized(self) -> bool:
        #Get count of database entities
        result = self.db.executeQuery(
        "MATCH (n) RETURN count(n) as count",
        Neo4JConnector.ontologyDatabasePath)

        #Check if there are any database entities.
        if result[0]["count"] > 0:
            #Get GraphConfig Entities
            result = self.db.executeQuery(
            "MATCH (n:_GraphConfig) RETURN count(n) as config",
            Neo4JConnector.ontologyDatabasePath)
            #Check if there are any GraphConfig entities. If not, GraphConfig needs to be initialized.
            if result[0]["config"] > 0:
                return True
        return False

    def loadOntology(self) -> bool:
        
        #Init GraphConfig. This is needed for the onto import.
        result = self.db.execute_query(
            "CALL n10s.graphconfig.init()",
            database_= Neo4JConnector.ontologyDatabasePath)
        
        #Import ontology from brick schem repo.
        print("Loadging brick ontology from: " + self.brickSchemaDownloadPath)
        result= self.db.executeQuery(
            "CALL n10s.onto.import.fetch(" + self.brickSchemaDownloadPath + "," + self.brickSchemaDownloadFileType + ")",
            Neo4JConnector.ontologyDatabasePath)
        
        print(result)
        
        
    def updateOntology(self) -> bool:
        #TODO Discuss if ueful
        pass

    def dropOntology(self) -> bool:
        result = self.db.executeQuery(
            "MATCH (n) DETACH DELETE n",
            Neo4JConnector.ontologyDatabasePath)
        return result[0]["terminationStatus"] == "OK"