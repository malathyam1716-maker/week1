from urllib.parse import urljoin, urlparse
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

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        stop=stop_after_attempt(5)
    )
    def __fetch_url(self, url, params=None):
        response = requests.get(url, headers=self.__headers, params=params)
        response.raise_for_status()
        return response.json()

    def __salesForce_client(self, query):
        url = f"{self.__base_url}query/"
        params = {"q": query}
        all_records = []

        while True:
            try:
                data = self.__fetch_url(url, params=params)
                records = data.get("records", [])
                all_records.extend(records)
                print(f"Extracted {len(records)} records from Salesforce. Total so far: {len(all_records)}")

                next_url = data.get("nextRecordsUrl")
                if not next_url or data.get("done", True):
                    break

                # Build full next URL using base_url's host
                parsed_base = urlparse(self.__base_url)
                base_host = f"{parsed_base.scheme}://{parsed_base.netloc}"
                url = urljoin(base_host, next_url)
                params = None  # query is embedded in nextRecordsUrl
            except Exception as e:
                raise Exception("Salesforce API error: " + str(e))

        return all_records

    def extract(self) -> list[dict]:
        data = self.__salesForce_client(self.query)
        return data
