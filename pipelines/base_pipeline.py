from abc import ABC, abstractmethod
from utils.validator import validator


class BasePipeline(ABC):
    model = None

    def run(self):
        data = self.extract()
        data = self.validate(data)
        data = self.transform(data)
        self.load(data)

    def validate(self, data):
        return validator(data, self.model)

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, data):
        pass
