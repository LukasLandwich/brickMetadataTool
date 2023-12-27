from abc import ABC, abstractmethod
from ontologyResource import OntologyResource, OntologyResourceInstance

class OntologyAdapter(ABC):
    
    @abstractmethod
    def getAllClasses(self) -> [OntologyResource]:
        pass
    
    @abstractmethod
    def getClass(self, name:str) -> OntologyResource:
        pass
    
    @abstractmethod
    def getAllRelationships(self) -> [OntologyResource]:
        pass
    
    @abstractmethod
    def getAllProperties(self) -> [OntologyResource]:
        pass
    
    @abstractmethod
    def getPossiblePropertiesOf(self, _class:str) -> [OntologyResource]:
        pass
    
    @abstractmethod
    def getPossibleRelationshipsOf(self, _class:str) -> [OntologyResource]:
        pass
    
    @abstractmethod
    def createNode(self, classInstance:OntologyResourceInstance) -> bool:
        pass
    
    @abstractmethod
    def isOntologyInitialized(self) -> bool:
        pass
    
    @abstractmethod
    def loadOntology(self) -> bool:
        pass
    
    @abstractmethod
    def updateOntology(self) -> bool:
        pass
    
    @abstractmethod
    def dropOntology(self) -> bool:
        pass