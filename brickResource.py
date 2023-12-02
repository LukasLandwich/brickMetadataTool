import json
from ontologyResource import OntologyResource, OntologyResourceInstance

class BrickResource(OntologyResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        self.name = name
        self.label = label
        self.definition = definition
        self.uri = uri
    
    def __str__(self) -> str:
        return self.name
    
    def serialize(self):
        return {"name": self.name, "label":self.label, "definition":self.definition, "uri":self.uri }
    
    def toJSON(self):
        return json.dumps( {"name": self.name, "label":self.label, "definition":self.definition, "uri":self.uri })
    


class BrickProperty(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)
        

class BrickRelationship(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)
        

        
class BrickClass(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)

        
        
class BrickRessourceInstance(OntologyResourceInstance):
    def getCreationQuery(self) -> str:
        pass

class BrickPropertyInstance(BrickRessourceInstance):
    def __init__(self, propertyResource:BrickProperty, value) -> None:
        self.propertyResource = propertyResource
        self.value = value

        
    def getCreationQuery(self) -> str:
        return "{}: '{}'".format(self.propertyResource.name ,str(self.value))
    
        
class BrickClassInstance(BrickRessourceInstance):
    def __init__(self, classResource:BrickClass, name:str, properties:[BrickPropertyInstance]) -> None:
        super().__init__()
        self.classResource = classResource
        self.name = name
        self.properties = properties if properties is not None  else []
        
    def getCreationQuery(self) -> str:
        if len(self.properties) == 0:
            propertyString = "{name: '" + self.name + "'}"
        else:
            propertyString = "{name: '" + self.name +"', " + ', '.join(p.getCreationQuery() for p in self.properties) + "}"
        return "CREATE (:{} {})".format(self.classResource.name ,propertyString)
 
        
class BrickRelationshipInstance(BrickRessourceInstance):
    def __init__(self, relationshipResource:BrickRelationship, _from:BrickClassInstance, _to:BrickClassInstance) -> None:
        super().__init__()
        self.relationshipResource = relationshipResource
        self._from = _from
        self._to = _to

