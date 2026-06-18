from abc import ABC, abstractmethod
from utils.validator import validator


class BasePipeline(ABC):
    model = None

    def run(self):
        data = self.extract()
        data = self.load_raw_data(data)
        data = self.validate(data)
        data = self.transform(data)
        self.load(data)

    def validate(self, data):
        return validator(data, self.model)

    @abstractmethod
    def extract(self,data):
        pass

    @abstractmethod
    def load_raw_data(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, data):
        pass
