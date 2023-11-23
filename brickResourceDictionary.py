from brickResource import BrickClass, BrickProperty, BrickRelationship
from brickadapter import BrickAdapter

class BrickResourceDictionaty:
    
    def __init__(self, db:BrickAdapter) -> None:
        self.classes = {x.name : x for x in db.getAllClasses()}
        self.properties = {x.name : x for x in db.getAllProperties()}
        self.relationships = {x.name : x for x in db.getAllRelationships()}
        
    def getClass(self, label:str) -> BrickClass:
        return self.classes.get(label)
    
    
    def getProperty(self, label:str) -> BrickProperty:
        return self.properties.get(label)
    
    
    def getReslationship(self, name:str) -> BrickRelationship:
        return self.relationships.get(name)
   

        