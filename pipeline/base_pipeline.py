from utils.validator import validator
from typing import Type
from pydantic import BaseModel

class BasePipeline:
    def __init__(self, 
                 name: str,
                 model: Type[BaseModel],
                 extractor,
                 transformer,
                 raw_loader,
                 final_loader):
        self.name = name
        self.model = model
        self.extractor = extractor
        self.transformer = transformer
        self.raw_loader = raw_loader
        self.final_loader = final_loader

    def run(self):
        # 1. Extract raw data from API
        raw_data = self.extractor.extract()
        
        # 2. Save raw data to S3 Data Lake and get the object key
        s3_key = self.raw_loader.load_raw_data(raw_data, prefix=self.name.lower())
        
        # 3. Read raw data back from S3
        s3_data = self.raw_loader.read_raw_data(s3_key)
        
        # If S3 is not configured, fallback to raw_data
        data_to_process = s3_data if s3_data else raw_data
        
        # 4. Validate and Transform
        validated_data = self.validate(data_to_process)
        transformed_data = self.transformer.transform(validated_data)
        
        # 5. Load to final destination (Data Warehouse)
        self.final_loader.load(transformed_data)
        return transformed_data

        
    def validate(self, data):
        return validator(data, self.model)
