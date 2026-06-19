import requests

class ZenDeskExtractor:

    def __init__(self, base_url, access_token):
        self.__access_token = access_token
        self.__base_url = base_url
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }

    def __client(self, service_type, per_page=200):
        headers = self.__headers
        params = {
            "page": f"{per_page}  "
        }
        url = f"{self.__base_url}{service_type}/"
        try:
            while True:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                data = response.json()
                # records = data.get("records", [])
                print(data)
                # if len(records) < limit:
                #     break
                if data.get("has_more", True):
                     break
                return data


            # return records
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed request : {e}")

        
    def extract(self, query: str) -> list[dict]:
        data = self.__client(query)
        return data
