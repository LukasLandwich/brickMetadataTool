from neo4j import GraphDatabase, Result,NotificationSeverity
import logging

brickSchemaDB = "brickSchema"
metadataDB = "metadata"
brickSchemaDownloadPath = "'https://brickschema.org/schema/1.3.0/Brick.ttl'"
brickSchemaDownloadFileType = "'Turtle'"

class Neo4JConnector:

    log = logging.getLogger(__name__)
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)
            
    def create_entity(self, label:str):
        self.driver.execute_query()
            
    def hasBrickInitialized(self) -> bool:
        #Get count of database entities
        result, summary, keys = self.driver.execute_query(
        "MATCH (n) RETURN count(n) as count",
        database_= brickSchemaDB)

        #Check if there are any database entities.
        if result[0]["count"] > 0:
            #Get GraphConfig Entities
            result, summary, keys = self.driver.execute_query(
            "MATCH (n:_GraphConfig) RETURN count(n) as config",
            database_= brickSchemaDB)
            #Check if there are any GraphConfig entities. If not, GraphConfig needs to be initialized.
            if result[0]["config"] > 0:
                return True
        return False
    
    def loadBrickOntology(self) -> bool:
        
        #Init GraphConfig. This is needed for the onto import.
        result, summary, keys = self.driver.execute_query(
            "CALL n10s.graphconfig.init()",
            database_= brickSchemaDB)
        
        #Import ontology from brick schem repo.
        print("Loadging brick ontology from: " + brickSchemaDownloadPath)
        result, summary, keys = self.driver.execute_query(
            "CALL n10s.onto.import.fetch(" + brickSchemaDownloadPath + "," + brickSchemaDownloadFileType + ")",
            database_= brickSchemaDB)
        
        print(result)
        
        
    def updateBrickOnotlogy(self) -> bool:
        #TODO Discuss if ueful
        pass
    
    def dropBrickOntology(self) -> bool:
        result, summary, keys = self.driver.execute_query(
            "MATCH (n) DETACH DELETE n",
            database_= brickSchemaDB)
        return result[0]["terminationStatus"] == "OK"
    
    def resultTransformer(result: Result):
        return result.values
    
    def executeQuery(self, query, database):
         result, summary, key = self.driver.execute_query(query, database_=database)
         self.handleSummary(summary)
         return result
    
    def handleSummary(self, summary):
        for notification in summary.summary_notifications:
            severity = notification.severity_level
            if severity == NotificationSeverity.WARNING:
                # or severity_level == "WARNING"
                self.log.warning("%r", notification)
            elif severity == NotificationSeverity.INFORMATION:
                # or severity_level == "INFORMATION"
                self.log.info("%r", notification)
            else:
                # assert severity == NotificationSeverity.UNKNOWN
                # or severity_level == "UNKNOWN"
                self.log.debug("%r", notification)
     








