import polars as pl
from models.unified import UnifiedCustomer, UnifiedTransaction
from utils.enums import StripeServiceEnum


class StripeTransformer:
    def __init__(self, record_type: StripeServiceEnum | str):
        self.record_type = self._normalize_record_type(record_type)

    @staticmethod
    def _normalize_record_type(record_type: StripeServiceEnum | str) -> StripeServiceEnum:
        if isinstance(record_type, StripeServiceEnum):
            return record_type

        normalized_value = (record_type or "").strip().lower()
        if normalized_value in {"customer", "customers"}:
            return StripeServiceEnum.customers
        if normalized_value in {"charge", "charges"}:
            return StripeServiceEnum.charges
        return StripeServiceEnum.customers

    def transform(self, data: list[dict]):
        if self.record_type == StripeServiceEnum.customers:
            return self.__transform_customers(data)
        if self.record_type == StripeServiceEnum.charges:
            return self.__transform_charges(data)
        return []

    def __transform_customers(self, data: list[dict]) -> list[UnifiedCustomer]:
        if not data:
            return []
            
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

        df = pl.DataFrame(data)
        
        df = df.with_columns([
            pl.col("name").fill_null("Unknown"),
            (pl.col("created_unix") * 1000).cast(pl.Datetime(time_unit="ms")).alias("created_at")
        ])
        
        df_unified = df.select([
            pl.col("customer_id").cast(pl.Utf8).alias("id"),
            pl.lit("stripe").alias("source_system"),
            pl.col("name"),
            pl.col("email").cast(pl.Utf8),
            pl.col("phone").cast(pl.Utf8),
            pl.col("created_at"),
            pl.lit(None).alias("updated_at")
        ])
        
        unified_dicts = df_unified.to_dicts()
        return [UnifiedCustomer(**d) for d in unified_dicts]

    def __transform_charges(self, data: list[dict]) -> list[UnifiedTransaction]:
        if not data:
            return []
            
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

        df = pl.DataFrame(data)
        
        df = df.with_columns([
            (pl.col("amount_in_cents") / 100.0).alias("amount"),
            (pl.col("created_unix") * 1000).cast(pl.Datetime(time_unit="ms")).alias("created_at")
        ])
        
        df_unified = df.select([
            pl.col("charge_id").cast(pl.Utf8).alias("id"),
            pl.lit("stripe").alias("source_system"),
            pl.col("customer_id").cast(pl.Utf8).fill_null("Unknown"),
            pl.col("amount"),
            pl.col("currency").cast(pl.Utf8),
            pl.col("status").cast(pl.Utf8),
            pl.col("created_at"),
            pl.lit(None).alias("updated_at")
        ])
        
        unified_dicts = df_unified.to_dicts()
        return [UnifiedTransaction(**d) for d in unified_dicts]
