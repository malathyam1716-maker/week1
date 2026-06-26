from abc import ABC, abstractmethod

class RawDataLoader(ABC):
    @abstractmethod
    def load_raw_data(self, data: list[dict], prefix: str) -> str:
        pass

    @abstractmethod
    def read_raw_data(self, file_name: str) -> list[dict]:
        pass

class FinalDataLoader(ABC):
    @abstractmethod
    def load(self, data: list[dict]):
        pass
