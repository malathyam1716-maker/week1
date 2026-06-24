from stripe import StripeClient
from enum import Enum
from tenacity import retry, wait_exponential, stop_after_attempt

class ServiceEnum(Enum):
    customers = "customers" 
    charges = "charges"

class StripeExtractor:  
    def __init__(self, api_key: str, service_type: ServiceEnum):
        self.api_key = api_key
        self.service_type = service_type

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def __client(self,service_type:ServiceEnum) -> list[dict]:
        client = StripeClient(self.api_key)
        service = getattr(client.v1, service_type.value,"customers")
        data = service.list().data
        return data
        
    
    def extract(self) -> list[dict]:
        raw_data = self.__client(self.service_type)
        customer_list = [c.to_dict() for c in raw_data]
        return customer_list

