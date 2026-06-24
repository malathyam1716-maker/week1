import requests
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception
from utils.exception_handling import is_retryable_exception
from config.settings import settings

class SalesForceExtractor:

    def __init__(self, base_url:str, access_point:str, query: str):
        self.__base_url = base_url
        self.__access_token = access_point
        self.query = query
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }

    # @retry(retry=retry_if_exception(is_retryable_exception), wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def __salesForce_client(self, query, limit=2000):
        headers = self.__headers
        params = {
            "q": f"{query}  "
        }
        url = f"{self.__base_url}query/"
        
        while True:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                data = response.json()
                records = data.get("records", [])
                print(f"Extracted {len(records)} records from Salesforce.")
                
                return records
            except Exception as e:
                raise Exception("Salesforce api error " + str(e))
        
    def extract(self) -> list[dict]:
        data = self.__salesForce_client(self.query)
        return data
