import polars as pl
from models.unified import UnifiedCustomer
from utils.enums import SalesForceServiceEnum


class SalesForceTransformer:
    def __init__(self, record_type: SalesForceServiceEnum | str):
        self.record_type = self._normalize_record_type(record_type)

    @staticmethod
    def _normalize_record_type(record_type: SalesForceServiceEnum | str) -> SalesForceServiceEnum:
        if isinstance(record_type, SalesForceServiceEnum):
            return record_type

        normalized_value = (record_type or "").strip().lower()
        if normalized_value in {"account", "accounts"}:
            return SalesForceServiceEnum.accounts
        if normalized_value in {"contact", "contacts"}:
            return SalesForceServiceEnum.contacts
        return SalesForceServiceEnum.accounts

    def transform(self, data: list[dict]) -> list[UnifiedCustomer]:
        if self.record_type == SalesForceServiceEnum.accounts:
            return self.__transform_accounts(data)
        if self.record_type == SalesForceServiceEnum.contacts:
            return self.__transform_contact(data)
        return []

    def __transform_accounts(self, data: list[dict]) -> list[UnifiedCustomer]:
        if not data:
            return []
            
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

        df = pl.DataFrame(data)
        
        df = df.with_columns([
            pl.col("Name").fill_null("Unknown")
        ])
        
        df_unified = df.select([
            pl.col("Id").cast(pl.Utf8).alias("id"),
            pl.lit("salesforce").alias("source_system"),
            pl.col("Name").alias("name"),
            pl.lit(None).alias("email"), 
            pl.lit(None).alias("phone"), 
            pl.col("CreatedDate").cast(pl.Datetime).alias("created_at"),
            pl.col("LastModifiedDate").cast(pl.Datetime).alias("updated_at")
        ])
        
        unified_dicts = df_unified.to_dicts()
        return [UnifiedCustomer(**d) for d in unified_dicts]

    def __transform_contact(self, data: list[dict]) -> list[UnifiedCustomer]:
        if not data:
            return []
            
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

        df = pl.DataFrame(data)
        
        df = df.with_columns([
            pl.concat_str([pl.col("FirstName").fill_null(""), pl.lit(" "), pl.col("LastName").fill_null("")]).str.strip_chars().alias("name")
        ])
        
        df_unified = df.select([
            pl.col("Id").cast(pl.Utf8).alias("id"),
            pl.lit("salesforce").alias("source_system"),
            pl.col("name"),
            pl.col("Email").cast(pl.Utf8).alias("email"),
            pl.col("Phone").cast(pl.Utf8).alias("phone"),
            pl.col("CreatedDate").cast(pl.Datetime).alias("created_at"),
            pl.col("LastModifiedDate").cast(pl.Datetime).alias("updated_at")
        ])
        
        unified_dicts = df_unified.to_dicts()
        return [UnifiedCustomer(**d) for d in unified_dicts]
