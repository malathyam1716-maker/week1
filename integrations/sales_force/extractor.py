import requests
from typing import Type
from pydantic import BaseModel

class SalesForce:
    def __init__(self, base_url, access_token):
        self.__access_token = access_token
        self.__base_url = base_url
        self.__headers = {
            "Authorization": f"Bearer {self.__access_token}",
            "Content-Type": "application/json"
        }
    def __extract_data(self, query, limit=2000, offset=0):
        headers = self.__headers
        params = {
            "q": f"{query} LIMIT {limit} OFFSET {offset}"
        }
        try:
            response = requests.get(f"{self.__base_url}query/", headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to extract data: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")

        
    def extract(self, query:str) -> list[dict]:
        data = self.__extract_data(query)
        return data.get("records", [])

    def validate(self, data:list[dict], model_class : Type[BaseModel]) -> list[dict]:
        if not data:
            return []
        print(data)
        return [model_class.model_validate(record).model_dump() for record in data]
