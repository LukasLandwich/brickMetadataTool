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
        self.resource = propertyResource
        self.value = value
        
    def __str__(self) -> str:
        return self.resource.name + ": " + self.value
    
    def serialize(self):
        pass
    
    def toJSON(self):
        pass

    
        
class BrickClassInstance(OntologyResourceInstance):
    def __init__(self, classResource:BrickResource, name:str, properties:[BrickPropertyInstance], id:int = None) -> None:
        self.resource = classResource
        self.name = name
        self.properties = properties if properties is not None  else []
        self.id = id
        
    def __str__(self) -> str:
        return self.name + ":" + self.resource.name + "{" + ", ".join([str(p) for p in self.properties]) + "}"
    
    def serialize(self):
        return {"name": self.name, "id":self.id, "class":self.resource.name, "properties": {p.resource.name : p.value for p in self.properties}}
    
    def toJSON(self):
        return json.dumps( {"name": self.name, "id":self.id, "class":self.resource.name})
 
        
class BrickRelationshipInstance(OntologyResourceInstance):
    def __init__(self, relationshipResource:BrickResource, _from:BrickClassInstance, _to:BrickClassInstance) -> None:
        self.resource = relationshipResource
        self._from = _from
        self._to = _to
        
    def __str__(self) -> str:
        return str(self._from) + "-[:" + self.resource.name +"]-" + str(self._to)
    
    def serialize(self):
        pass
    
    def toJSON(self):
        pass

