from abc import ABC, abstractmethod

class OntologyResource(ABC):
        
    @abstractmethod
    def __str__(self) -> str:
        pass
        
    @abstractmethod
    def serialize(self) -> dict:
        pass
        
    @abstractmethod
    def toJSON(self) -> str:
        pass
    
class OntologyResourceInstance(ABC):
    pass