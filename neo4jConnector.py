from neo4j import GraphDatabase, NotificationSeverity, Record, ResultSummary
import logging

class Neo4JConnector:

    ontologyDatabasePath = "brickSchema"
    metadataDatabasePath = "metadata"
    propertyStoreDatabasePath = "propertystore"
    
    log = logging.getLogger(__name__)
    
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> bool:
        self.driver.close()
                        
    def executeQuery(self, query, database) -> [Record]:
         result, summary, key = self.driver.execute_query(query, database_=database)
         self.handleSummary(summary)
         return result
    
    def handleSummary(self, summary:ResultSummary) -> None:
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
     








