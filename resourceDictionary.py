from OntologyAdapter import OntologyAdapter
from ontologyResource import OntologyResource

class ResourceDictionaty:
    
    def __init__(self, db:OntologyAdapter) -> None:
        self.classes = {x.name : x for x in db.getAllClasses()}
        self.properties = {x.name : x for x in db.getAllProperties()}
        self.relationships = {x.name : x for x in db.getAllRelationships()}
        
    def getClass(self, label:str) -> OntologyResource:
        return self.classes.get(label)
    
    
    def getProperty(self, label:str) -> OntologyResource:
        return self.properties.get(label)
    
    
    def getReslationship(self, name:str) -> OntologyResource:
        return self.relationships.get(name)
   

        