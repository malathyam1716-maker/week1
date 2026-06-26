import requests
from tenacity import retry, wait_exponential, stop_after_attempt
from config.settings import settings

class ZenDeskExtractor:

    def __init__(self):
        self.__access_token = settings.zendesk_access_token
        self.__base_url = settings.zendesk_endpoint
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def __client(self, service_type, per_page=200):
        headers = self.__headers
        params = {
            "per_page": per_page
        }
        url = f"{self.__base_url}{service_type}/"
        
        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            print(f"Extracted data from Zendesk: {service_type}")
            
            if not data.get("has_more", False):
                 break
            # TODO: handle actual pagination state
            return data

        return data

        
    def extract(self, query: str) -> list[dict]:
        data = self.__client(query)
        return [data] if isinstance(data, dict) else data
