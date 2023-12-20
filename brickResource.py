import json
from ontologyResource import OntologyResource, OntologyResourceInstance
from brickResourceType import BrickResourceType

class BrickResource(OntologyResource):  
    
    def __init__(self, name:str, label:str, definition:str, uri:str, type:BrickResourceType) -> None:
        self.name = name
        self.label = label
        self.definition = definition
        self.uri = uri
        self.type = type
    
    def __str__(self) -> str:
        return self.name
    
    def serialize(self):
        return {"name": self.name, "label":self.label, "definition":self.definition, "uri":self.uri }
    
    def toJSON(self):
        return json.dumps( {"name": self.name, "label":self.label, "definition":self.definition, "uri":self.uri })      
        
class BrickPropertyInstance(OntologyResourceInstance):
    def __init__(self, propertyResource:BrickResource, value) -> None:
        self.propertyResource = propertyResource
        self.value = value
    
        
class BrickClassInstance(OntologyResourceInstance):
    def __init__(self, classResource:BrickResource, name:str, properties:[BrickPropertyInstance]) -> None:
        self.classResource = classResource
        self.name = name
        self.properties = properties if properties is not None  else []
 
        
class BrickRelationshipInstance(OntologyResourceInstance):
    def __init__(self, relationshipResource:BrickResource, _from:BrickClassInstance, _to:BrickClassInstance) -> None:
        self.relationshipResource = relationshipResource
        self._from = _from
        self._to = _to

