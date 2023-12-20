from brickResource import BrickResource, BrickClassInstance
from neo4jConnector import Neo4JConnector
from brickResourceType import BrickResourceType
from ontologyAdapter import OntologyAdapter

class BrickAdapter(OntologyAdapter):
       
    brickSchemaDownloadPath = "'https://brickschema.org/schema/1.3.0/Brick.ttl'"
    brickSchemaDownloadFileType = "'Turtle'"
    
    def __init__(self, db:Neo4JConnector) -> None:
        self.db = db
        
        if not self.isOntologyInitialized():
            print("Brick Onntology isnt initilaized.")
            self.loadOntology()
  
    def getAllClasses(self) -> [BrickResource]:
        classes = self.db.executeQuery(
        "MATCH (a:n4sch__Class) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickResource(resource["name"], resource["label"], resource["definition"], resource["uri"], BrickResourceType.CLASS))
            
        return classesList
    
  
    def getAllRelationships(self) -> [BrickResource]:
        relationships = self.db.executeQuery(
        "MATCH (a:n4sch__Relationship) RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        relationshipsList = []
        for resource in relationships:
            relationshipsList.append(BrickResource(resource["name"], resource["label"], resource["definition"], resource["uri"], BrickResourceType.RELATIONSHIP))
            
        return relationshipsList
    
    def getAllProperties(self) -> [BrickResource]:
        properties = self.db.executeQuery(
        "MATCH (a:Resource) WHERE SIZE(LABELS(a)) = 1 RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickResource(resource["name"], resource["label"], resource["definition"], resource["uri"], BrickResourceType.PROPERTY))
            
        return propertiesList
    
    def getAllShpaes(self) -> [BrickResource]:
        #TODO Implement if needed
        #match (a) -[:n4sch__DOMAIN]- (b) - [:n4sch__RANGE] - (c)-[]-(d) where a.n4sch__label= "Building" return a,b,c,d
        pass
    
    def getPossiblePropertiesOf(self, _class:str) -> [BrickResource]:  
        query =  """MATCH (p)- [:n4sch__DOMAIN] ->(b)<-[:n4sch__SCO*0..5]-(a:n4sch__Class) where SIZE(LABELS(p)) = 1 and a.n4sch__name='{className}' RETURN Distinct p.n4sch__name as name, p.n4sch__label as label, p.n4sch__definition as definition, p.uri as uri""".format(className = _class)
        print(query)
        properties = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        propertiesList = []
        for resource in properties:
            propertiesList.append(BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.PROPERTY))
        return propertiesList      
        
    def getPossibleRelationshipsOf(self, _class:str) -> [BrickResource]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = '{className}'  Return Distinct pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__definition as definition, pcrel.uri as uri""".format(className = _class)
        relationships = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.RELATIONSHIP))
        return relationshipList
    
    def getClass(self, name:str) -> BrickResource:
        query = """match (c:n4sch__Class) where c.n4sch__label = '{className}' Return c.n4sch__name as name, c.n4sch__label as label, c.n4sch__defintion as definition, c.uri as uri""".format(className = name) 
        brickClass = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        resource = brickClass[0]
        return BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.CLASS)
    
    def createNode(self, classisntance:BrickClassInstance, database) -> bool:
        query = self.getCreationQuery(classisntance)
        relationships = self.db.executeQuery(query,database)
        #TODO handle response and return fitting bool
        return True
        
    
    
    def createRelationship(self, type:str, _from:str):
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
        #TODO Use Constraint
        #CREATE CONSTRAINT n10s_unique_uri ON (r:Resource)
#ASSERT r.uri IS UNIQUE;
        
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
    
    
    #---------------------Query Creators----------------------
    def getCreationQuery(self, res: BrickResource) -> str:
        if res.type == BrickResourceType.CLASS:
            return "{}: '{}'".format(res.propertyResource.name ,str(res.value))
        elif res.type == BrickResourceType.PROPERTY:
            if len(res.properties) == 0:
                propertyString = "{name: '" + res.name + "'}"
            else:
                propertyString = "{name: '" + res.name +"', " + ', '.join(self.getCreationQuery(p) for p in res.properties) + "}"
            return "CREATE (:{} {})".format(res.classResource.name ,propertyString)
        elif res.type == BrickResourceType.RELATIONSHIP:
            pass
        else:
            print("Unknow Brick Resoruce Type. Please check and/or change implementaiton.")