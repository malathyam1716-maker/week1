from abc import ABC, abstractmethod


class BasePipeline(ABC):

    def run(self):
        data = self.extract()
        data = self.validate(data)
        data = self.transform(data)
        self.load(data)

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def validate(self, data):
        pass

    @abstractmethod
    def transform(self, data):
        pass

    @abstractmethod
    def load(self, data):
        pass