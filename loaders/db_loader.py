from loaders.base_loader import FinalDataLoader

class DBLoader(FinalDataLoader):
    def load(self, data: list[dict]):
        print(f"Loaded {len(data)} records to destination.")
