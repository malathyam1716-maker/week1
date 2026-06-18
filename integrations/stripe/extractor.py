from stripe import StripeClient
from enum import Enum

class ServiceEnum(Enum):
    customers = "customers" 
    charges = "charges"

class StripeExtractor:  
    def __init__(self,api_key):
        self.api_key = api_key

    def __client(self,service_type:ServiceEnum) -> list[dict]:
        client = StripeClient(self.api_key)
        service = getattr(client.v1, service_type.value,"customers")
        data = service.list().data
        return data
        
    
    def extract(self, service_type: ServiceEnum) -> list[dict]:
        raw_data = self.__client(service_type)
        customer_list = [c.to_dict() for c in raw_data]
        return customer_list

