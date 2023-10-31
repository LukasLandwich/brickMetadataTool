from neo4j import GraphDatabase

brickSchemaDB = "brickSchema"
metadataDB = "metadata"
brickSchemaDownloadPath = "'https://brickschema.org/schema/1.3.0/Brick.ttl'"
brickSchemaDownloadFileType = "'Turtle'"

class Neo4JConnector:

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
        self.driver.execute_query(
            "CALL n10s.graphconfig.init()",
            database_= brickSchemaDB)
        
        #Import ontology from brick schem repo.
        print("Loadging brick ontology from: " + brickSchemaDownloadPath)
        self.driver.execute_query(
            "CALL n10s.onto.import.fetch(" + brickSchemaDownloadPath + "," + brickSchemaDownloadFileType + ")",
            database_= brickSchemaDB)
        
    def updateBrickOnotlogy(self) -> bool:
        #TODO Discuss if ueful
        pass
    
    def dropBrickOntology(self) -> bool:
        pass
    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]