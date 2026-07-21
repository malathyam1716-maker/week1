import sys
from sqlalchemy import create_engine, Column, String, Float, DateTime, inspect
from sqlalchemy.orm import declarative_base, sessionmaker
from loaders.base_loader import FinalDataLoader
from models.unified import UnifiedCustomer, UnifiedTransaction
from config.settings import settings

Base = declarative_base()

class DbCustomer(Base):
    __tablename__ = "unified_customers"

    id = Column(String, primary_key=True)
    source_system = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class DbTransaction(Base):
    __tablename__ = "unified_transactions"

    id = Column(String, primary_key=True)
    source_system = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

class DBLoader(FinalDataLoader):
    def __init__(self, database_url: str = None):
        self.database_url = database_url or settings.database_url or "sqlite:///data_warehouse.db"
        print(f"DB Loader initializing with connection URL: {self.database_url}")
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def load(self, data: list[UnifiedCustomer | UnifiedTransaction]):
        if not data:
            print("DB Loader: No records to load.")
            return

        session = self.Session()
        dialect = self.engine.dialect.name
        print(f"DB Loader: Loading {len(data)} records via upsert into {dialect} Data Warehouse...")

        try:
            first_record = data[0]
            if isinstance(first_record, UnifiedCustomer):
                model_class = DbCustomer
                primary_keys = ["id", "source_system"]
            elif isinstance(first_record, UnifiedTransaction):
                model_class = DbTransaction
                primary_keys = ["id", "source_system"]
            else:
                raise ValueError(f"Unsupported record type: {type(first_record)}")

            # Convert Pydantic models to dicts
            record_dicts = [record.model_dump() if hasattr(record, "model_dump") else record for record in data]

            if dialect == "postgresql":
                from sqlalchemy.dialects.postgresql import insert as pg_insert
                chunk_size = 1000
                for i in range(0, len(record_dicts), chunk_size):
                    chunk = record_dicts[i : i + chunk_size]
                    stmt = pg_insert(model_class).values(chunk)
                    update_cols = {c.name: c for c in stmt.excluded if c.name not in primary_keys}
                    stmt = stmt.on_conflict_do_update(
                        index_elements=primary_keys,
                        set_=update_cols
                    )
                    session.execute(stmt)
            elif dialect == "sqlite":
                from sqlalchemy.dialects.sqlite import insert as sqlite_insert
                chunk_size = 1000
                for i in range(0, len(record_dicts), chunk_size):
                    chunk = record_dicts[i : i + chunk_size]
                    stmt = sqlite_insert(model_class).values(chunk)
                    update_cols = {c.name: c for c in stmt.excluded if c.name not in primary_keys}
                    stmt = stmt.on_conflict_do_update(
                        index_elements=primary_keys,
                        set_=update_cols
                    )
                    session.execute(stmt)
            else:
                # Generic insert-or-update fallback
                for row in record_dicts:
                    filter_args = {pk: row[pk] for pk in primary_keys}
                    existing = session.query(model_class).filter_by(**filter_args).first()
                    if existing:
                        for k, v in row.items():
                            setattr(existing, k, v)
                    else:
                        session.add(model_class(**row))

            session.commit()
            print(f"DB Loader: Successfully upserted {len(data)} records to Table: {model_class.__tablename__}")
        except Exception as e:
            session.rollback()
            print(f"DB Loader: Failed to upsert records: {e}")
            raise e
        finally:
            session.close()
