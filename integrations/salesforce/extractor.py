import requests
from tenacity import retry, wait_exponential, stop_after_attempt
class SalesForceExtractor:

    def __init__(self, base_url: str, access_token: str, query: str):
        self.__access_token = access_token
        self.__base_url = base_url
        self.query = query
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(5))
    def __salesForce_client(self, query, limit=2000):
        headers = self.__headers
        params = {
            "q": f"{query}  "
        }
        url = f"{self.__base_url}query/"
        
        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            records = data.get("records", [])
            print(f"Extracted {len(records)} records from Salesforce.")
            
            # TODO: handle pagination properly if needed
            return records

        
    def extract(self) -> list[dict]:
        data = self.__salesForce_client(self.query)
        return data
