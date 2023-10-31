class BrickResource:
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        self.name = name
        self.label = label
        self.definition = definition
        self.uri = uri
    
    def __str__(self) -> str:
        return self.name
    
class BrickClass(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)

class BrickProperty(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)

class BrickRelationship(BrickResource):
    def __init__(self, name:str, label:str, definition:str, uri:str) -> None:
        super().__init__(name, label, definition, uri)