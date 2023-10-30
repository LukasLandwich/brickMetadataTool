from services.service import Service

class ServiceController():
    def __init__(self, serviecCollection):
        if serviecCollection != None:
            self.services = serviecCollection
        else:
            self.services = dict()

    def get_services(self):
        if self.services != None:
            return self.services
        return dict()
    
    def add_service(self, service:Service):
        if self.services != None and service != None:
            self.services.update(service.name, service)
            return True
        return False
    
    def delete_service(self, service:Service):
        if self.services != None and service != None:
            self.services.pop(service.name)
            return True
        return False
            
    def delete_service(self, service:str):
        if self.services != None and service:
            self.services.pop(service)
            return True
        return False