import requests
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception
from config.settings import settings
from utils.exception_handling import is_retryable_exception

class ZenDeskExtractor:

    def __init__(self, service_type: str):
        self.service_type = service_type
        self.__access_token = settings.zendesk_access_token
        self.__base_url = settings.zendesk_endpoint
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

    def __client(self, service_type, per_page=100):
        # Format base URL correctly
        base_url = self.__base_url
        if not base_url.endswith("/"):
            base_url += "/"

        # Support appending .json to endpoint URL
        resource = service_type
        if not resource.endswith(".json"):
            resource += ".json"

        url = f"{base_url}{resource}"
        params = {"per_page": per_page}
        all_records = []

        while url:
            try:
                data = self.__fetch_url(url, params=params)
                # Zendesk returns records nested under a key corresponding to the resource type (e.g. "users")
                records = data.get(service_type, [])
                all_records.extend(records)
                print(f"Extracted {len(records)} records from Zendesk {service_type}. Total so far: {len(all_records)}")

                # Check pagination
                links = data.get("links", {})
                next_url = links.get("next") or data.get("next_page")
                if next_url:
                    url = next_url
                    params = None  # next_url contains all parameters
                else:
                    url = None
            except Exception as e:
                raise Exception(f"Zendesk API error: {e}")

        return all_records

    def extract(self) -> list[dict]:
        return self.__client(self.service_type)
