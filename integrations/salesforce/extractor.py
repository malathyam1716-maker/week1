import requests

class SalesForceExtractor:

    def __init__(self, base_url, access_token):
        self.__access_token = access_token
        self.__base_url = base_url
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }

    def __salesForce_client(self, query, limit=2000):
        all_records = []
        offset = 0

        headers = self.__headers
        params = {
            "q": f"{query} LIMIT {limit} OFFSET {offset}"
        }
        try:
            while True:
                response = requests.get(f"{self.__base_url}query/", headers=headers, params=params)
                response.raise_for_status()

                data = response.json()
                records = data.get("records", [])

                all_records.extend(records)
                print(records)
                if len(records) < limit:
                    break
                print(f"Records get : {offset} ")
                offset += limit

            return all_records
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed request : {e}")

        
    def extract(self, query: str) -> list[dict]:
        data = self.__salesForce_client(query)
        return data
