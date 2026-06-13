from abc import ABC, abstractmethod


class Extractor(ABC):
    @abstractmethod
    def extract(self):
        pass

class Validator(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class Transform(ABC):
    @abstractmethod
    def transform(self, data):
        pass

class Loader(ABC):
    @abstractmethod
    def load(self, data):
        pass


class BasePipeline(Extractor,Validator,Transform,Loader):

    def run(self):
        data = self.extract()
        data = self.validate(data)
        data = self.transform(data)
        self.load(data)



