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

class BrickResourceInstance(OntologyResourceInstance):
    def __init__(self, resource:BrickResource) -> None:
        self.resource = resource
  
class BrickPropertyInstance(BrickResourceInstance):
    def __init__(self, propertyResource:BrickResource, value) -> None:
        self.resource = propertyResource
        self.value = value

    
        
class BrickClassInstance(BrickResourceInstance):
    def __init__(self, classResource:BrickResource, name:str, properties:[BrickPropertyInstance]) -> None:
        self.resource = classResource
        self.name = name
        self.properties = properties if properties is not None  else []
 
        
class BrickRelationshipInstance(BrickResourceInstance):
    def __init__(self, relationshipResource:BrickResource, _from:BrickClassInstance, _to:BrickClassInstance) -> None:
        self.resource = relationshipResource
        self._from = _from
        self._to = _to

