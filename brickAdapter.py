from brickResource import BrickResource, BrickClassInstance
from ontologyResource import OntologyResource, OntologyResourceInstance
from neo4jConnector import Neo4JConnector
from brickResourceType import BrickResourceType
from ontologyAdapter import OntologyAdapter
from quantities import getUnitFor
from relationshipInverses import getInverse

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
        "MATCH (a:n4sch__Class) where not a.n4sch__name =~'.*Shape.*' RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        )   
        classesList = []
        for resource in classes:
            classesList.append(BrickResource(resource["name"], resource["label"], resource["definition"], resource["uri"], BrickResourceType.CLASS))
            
        return classesList
    
    def getAllShapes(self) -> [BrickResource]:
        shapes = classes = self.db.executeQuery(
        "MATCH (a:n4sch__Class) where a.n4sch__name =~'.*Shape.*' RETURN a.n4sch__name as name, a.n4sch__label as label, a.n4sch__definition as definition, a.uri as uri",
        Neo4JConnector.ontologyDatabasePath,
        ) 
        shapesList = []
        for shape in shapes:
            shapesList.append(BrickResource(shape["name"], shape["label"], shape["definition"], shape["uri"], BrickResourceType.SHAPE))
            
        return shapesList
  
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
            prop = BrickResource(resource["name"], resource["label"], resource["definition"], resource["uri"], BrickResourceType.PROPERTY)
            propertiesList.append(prop)
            
        return propertiesList
    
    def getClass(self, name:str) -> BrickResource:
        query = """match (c:n4sch__Class) where c.n4sch__label = '{className}' Return c.n4sch__name as name, c.n4sch__label as label, c.n4sch__defintion as definition, c.uri as uri""".format(className = name) 
        brickClass = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        resource = brickClass[0]
        return BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.CLASS)
    
    def getPossiblePropertiesOf(self, _class:str) -> [(BrickResource, BrickResource)]:  
        query =  """MATCH (p)- [:n4sch__DOMAIN] ->(b)<-[:n4sch__SCO*0..5]-(a:n4sch__Class) where SIZE(LABELS(p)) = 1 and a.n4sch__name='{className}' RETURN Distinct p.n4sch__name as name, p.n4sch__label as label, p.n4sch__definition as definition, p.uri as uri""".format(className = _class)
        properties = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        propertiesList = []
        for resource in properties:
            prop = BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.PROPERTY)
            shape = self.getShapeOfProperty(prop)
            if shape != None:
                quantityName = shape.name.replace("Shape", "")
                print(quantityName)
                unit = getUnitFor(quantityName)
                print(unit)
            propertiesList.append((prop,shape))

        return propertiesList  
    
    def getShapeOfProperty(self, property:BrickResource) -> BrickResource:
        query = """MATCH (vs)<-[:n4sch__SCO*0..5]-(s)<-[:n4sch__RANGE]-(p) where p.n4sch__name ='{propertyName}' and vs.n4sch__name = "ValueShape" return s.n4sch__name as name, s.n4sch__label as label, s.n4sch__definition as definition, s.uri as uri""".format(propertyName = property.name)
        property = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        if len(property) > 0:
            resource = BrickResource(property[0]["name"] , property[0]["label"], property[0]["definition"], property[0]["uri"], BrickResourceType.SHAPE)
            return resource
        else:
            return None
      
    def getPossibleRelationshipsOf(self, _class:str) -> [BrickResource]:
        query = """Match (pcrel:n4sch__Relationship) -[]- (pc:n4sch__Class) <-[:n4sch__SCO*0..4]- (c:n4sch__Class) where c.n4sch__name = '{className}'  Return Distinct pcrel.n4sch__name as name, pcrel.n4sch__label as label, pcrel.n4sch__definition as definition, pcrel.uri as uri""".format(className = _class)
        relationships = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        relationshipList = []
        for resource in relationships:
            relationshipList.append(BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.RELATIONSHIP))
        return relationshipList
    
    def getClassesInRangeOf(self, relationship: BrickResource) -> [BrickResource]:
        inverseName = getInverse(relationship.name)
        print(inverseName)
        query = """MATCH (r:n4sch__Relationship)- [:n4sch__DOMAIN] -(pc)<-[:n4sch__SCO*0..10]-(c:n4sch__Class)  where r.n4sch__name='{inverseName}' Return Distinct c.n4sch__name as name, c.n4sch__label as label, c.n4sch__definition as definition, c.uri as uri""".format(inverseName = inverseName)
        classes = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        classesList = []
        for resource in classes:
            classesList.append(BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.CLASS))
        return classesList
    
    def getRelationshipsWithNoOutgoingRel(self) -> [BrickResource]:
        query = "optional MATCH (n:n4sch__Relationship)-[r]->()return n.n4sch__name as name, n.n4sch__label as label, n.n4sch__definition as definition, n.uri as uri"
        result = self.db.executeQuery(query, Neo4JConnector.ontologyDatabasePath)
        relationshipsWithRel = []
        for resource in result:
            relationshipsWithRel.append(BrickResource(resource["name"] , resource["label"], resource["definition"], resource["uri"], BrickResourceType.RELATIONSHIP))
            
        allRelationships = self.getAllRelationships()
        without = []
        for rel in allRelationships:
            found = False
            for re in relationshipsWithRel:
                if rel.name == re.name:
                    found = True
            if not found:
               without.append(rel)         
        
        for w in without:
            if w.name in ["ambientTemperatureOfMeasurement", "hasAddress", "deprecationMigitationRule", "aggregationFunction" ]:
                without.remove(w)
                
        
        del without[3]
        return without
        
        
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
    
    
   