import json

class BrickResource:
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
        
        
class BrickRessourceInstance:
    pass

class BrickPropertyInstance(BrickRessourceInstance):
    def __init__(self, propertyResource:BrickProperty, value) -> None:
        super().__init__()
        self.propertyResource = propertyResource
        self.value = value
        
    def getCreationQuery(self) -> str:
        return self.getCreationQuery(self.propertyResource.label, self.value)
    
    @staticmethod
    def getCreationQuery(label, value):
        return "{}: '{}'".format(label ,str(value))
        
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
        return "CREATE (:{} {})".format(self.classResource.label ,propertyString)
    
    @staticmethod
    def getCreationQuery(name, label, properties):
        if len(properties) == 0:
            propertyString = "{name: '" + name + "'}"
        else:
            propertyString = "{name: '" + name +"', " + ', '.join(BrickPropertyInstance.getCreationQuery(p['label'], p['value']) for p in properties) + "}"
        return "CREATE (:{} {})".format(label , propertyString)
        
class BrickRelationshipInstance(BrickRessourceInstance):
    def __init__(self, relationshipResource:BrickRelationship, _from:BrickClassInstance, _to:BrickClassInstance) -> None:
        super().__init__()
        self.relationshipResource = relationshipResource
        self._from = _from
        self._to = _to

