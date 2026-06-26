import polars as pl
from models.unified import UnifiedCustomer

class ZenDeskTransformer:
    def transform(self, data: list[dict]) -> list[UnifiedCustomer]:
        return self.__transform_users(data)

    def __transform_users(self, data: list[dict]) -> list[UnifiedCustomer]:
        if not data:
            return []
            
        if not isinstance(data[0], dict):
            data = [d.model_dump() for d in data]

        df = pl.DataFrame(data)
        
        df = df.with_columns([
            pl.col("name").fill_null("Unknown")
        ])
        
        df_unified = df.select([
            pl.col("id").cast(pl.Utf8),
            pl.lit("zendesk").alias("source_system"),
            pl.col("name"),
            pl.col("email").cast(pl.Utf8),
            pl.col("phone").cast(pl.Utf8),
            pl.col("created_at").cast(pl.Datetime),
            pl.col("updated_at").cast(pl.Datetime)
        ])
        
        unified_dicts = df_unified.to_dicts()
        return [UnifiedCustomer(**d) for d in unified_dicts]
