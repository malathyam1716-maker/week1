from stripe import StripeClient
from enum import Enum

class ServiceEnum(Enum):
    accounts = "accounts"
    charges = "charges"

class StripeExtractor:  
    def __init__(self,api_key):
        self.api_key = api_key

    def __client(self,service_type:ServiceEnum):
        client = StripeClient(self.api_key)
        service = getattr(client.v1, service_type.value,"customers")
        data = service.list()
        return data
        
    
    def extract(self,service_type:ServiceEnum):
        raw_data = self.__client(service_type)

