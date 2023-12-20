from ontologyAdapter import OntologyAdapter
from ontologyResource import OntologyResource

class ResourceDictionaty:
    
    def __init__(self, db:OntologyAdapter) -> None:
        self.classes = dict(sorted({x.name : x for x in db.getAllClasses()}.items()))
        self.properties = dict(sorted({x.name : x for x in db.getAllProperties()}.items()))
        self.relationships = dict(sorted({x.name : x for x in db.getAllRelationships()}.items()))
        
    def getClass(self, label:str) -> OntologyResource:
        return self.classes.get(label)
    
    
    def getProperty(self, label:str) -> OntologyResource:
        return self.properties.get(label)
    
    
    def getReslationship(self, name:str) -> OntologyResource:
        return self.relationships.get(name)
    
    def getSortedClasses(self) -> [OntologyResource]:
        classes = [x for x in self.classes.keys()]
        classes = sorted(classes)
        return classes
   
