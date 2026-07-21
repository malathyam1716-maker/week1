import pytest
import datetime
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from loaders.db_loader import DBLoader, DbCustomer, DbTransaction
from loaders.s3_loader import S3Loader
from models.unified import UnifiedCustomer, UnifiedTransaction

from integrations.stripe.extractor import StripeExtractor
from integrations.salesforce.extractor import SalesForceExtractor
from integrations.zendesk.extractor import ZenDeskExtractor

from pipeline.pipelines import (
    get_stripe_customer_pipeline,
    get_stripe_charge_pipeline,
    get_salesforce_account_pipeline,
    get_salesforce_contact_pipeline,
    get_zendesk_user_pipeline
)

@pytest.fixture
def memory_db_loader():
    # Return a DBLoader that points to an in-memory SQLite database
    return DBLoader(database_url="sqlite:///:memory:")

@pytest.fixture
def mock_s3_loader():
    loader = MagicMock(spec=S3Loader)
    # Simulate S3 fallback behavior by returning None for s3_key,
    # which causes pipeline to fall back to the original in-memory extraction data
    loader.load_raw_data.return_value = None
    loader.read_raw_data.return_value = []
    return loader


def test_db_loader_upsert(memory_db_loader):
    # Setup database loader
    loader = memory_db_loader

    # Create dummy customer data
    cust1 = UnifiedCustomer(
        id="c1",
        source_system="stripe",
        name="John Doe",
        email="john@doe.com",
        phone="12345",
        created_at=datetime.datetime(2023, 1, 1, 12, 0, 0),
        updated_at=None
    )
    cust2 = UnifiedCustomer(
        id="c2",
        source_system="stripe",
        name="Jane Doe",
        email="jane@doe.com",
        phone="54321",
        created_at=datetime.datetime(2023, 1, 2, 12, 0, 0),
        updated_at=None
    )

    # 1. Insert records
    loader.load([cust1, cust2])

    session = loader.Session()
    db_records = session.query(DbCustomer).all()
    assert len(db_records) == 2
    
    # Verify values
    db_c1 = session.query(DbCustomer).filter_by(id="c1", source_system="stripe").one()
    assert db_c1.name == "John Doe"
    assert db_c1.email == "john@doe.com"

    # 2. Update values and run upsert (test incremental load)
    cust1_updated = UnifiedCustomer(
        id="c1",
        source_system="stripe",
        name="John Doe Updated",
        email="john.updated@doe.com",
        phone="12345",
        created_at=datetime.datetime(2023, 1, 1, 12, 0, 0),
        updated_at=datetime.datetime(2023, 1, 3, 12, 0, 0)
    )
    loader.load([cust1_updated])

    # Re-query
    db_records_after = session.query(DbCustomer).all()
    assert len(db_records_after) == 2  # Count remains same (no duplicates)
    
    db_c1_updated = session.query(DbCustomer).filter_by(id="c1", source_system="stripe").one()
    assert db_c1_updated.name == "John Doe Updated"
    assert db_c1_updated.email == "john.updated@doe.com"
    assert db_c1_updated.updated_at is not None

    session.close()


@patch("integrations.stripe.extractor.StripeClient")
def test_stripe_customer_pipeline(mock_stripe_client_class, mock_s3_loader, memory_db_loader):
    # Setup mocks
    mock_client = MagicMock()
    mock_stripe_client_class.return_value = mock_client
    
    mock_customer_data = [
        MagicMock(id="cus_1", name="Alex Jones", email="alex@jones.com", phone="111", created=1672531200, balance=0, to_dict=lambda: {
            "id": "cus_1", "object": "customer", "name": "Alex Jones", "email": "alex@jones.com", "phone": "111", "created": 1672531200, "balance": 0
        })
    ]
    
    # Mock service.list().data and has_more
    mock_page = MagicMock()
    mock_page.data = mock_customer_data
    mock_page.has_more = False
    mock_client.v1.customers.list.return_value = mock_page

    # Get pipeline and run
    pipeline = get_stripe_customer_pipeline(mock_s3_loader, memory_db_loader)
    pipeline.run()

    # Verify db contents
    session = memory_db_loader.Session()
    db_customers = session.query(DbCustomer).all()
    assert len(db_customers) == 1
    assert db_customers[0].id == "cus_1"
    assert db_customers[0].source_system == "stripe"
    assert db_customers[0].name == "Alex Jones"
    assert db_customers[0].email == "alex@jones.com"
    session.close()


@patch("integrations.salesforce.extractor.requests.get")
def test_salesforce_account_pipeline(mock_requests_get, mock_s3_loader, memory_db_loader):
    # Setup mocked HTTP response for Salesforce API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "done": True,
        "nextRecordsUrl": None,
        "records": [
            {
                "Id": "sf_acc_1",
                "Name": "Salesforce Corp",
                "Type": "Partner",
                "AccountNumber": "ACC123",
                "CreatedDate": "2023-01-01T12:00:00.000+0000",
                "LastModifiedDate": "2023-01-02T12:00:00.000+0000"
            }
        ]
    }
    mock_requests_get.return_value = mock_response

    # Run pipeline
    pipeline = get_salesforce_account_pipeline(mock_s3_loader, memory_db_loader)
    pipeline.run()

    # Verify database
    session = memory_db_loader.Session()
    db_customers = session.query(DbCustomer).all()
    assert len(db_customers) == 1
    assert db_customers[0].id == "sf_acc_1"
    assert db_customers[0].source_system == "salesforce"
    assert db_customers[0].name == "Salesforce Corp"
    session.close()


@patch("integrations.zendesk.extractor.requests.get")
def test_zendesk_user_pipeline(mock_requests_get, mock_s3_loader, memory_db_loader):
    # Setup mocked response for Zendesk users API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "users": [
            {
                "id": "zd_user_99",
                "name": "Zendesk User",
                "email": "zd@example.com",
                "phone": 12345,
                "role": "end-user",
                "active": True,
                "created_at": "2023-01-01T12:00:00Z",
                "updated_at": "2023-01-02T12:00:00Z"
            }
        ],
        "links": {"next": None}
    }
    mock_requests_get.return_value = mock_response

    # Run pipeline
    pipeline = get_zendesk_user_pipeline(mock_s3_loader, memory_db_loader)
    pipeline.run()

    # Verify database
    session = memory_db_loader.Session()
    db_customers = session.query(DbCustomer).all()
    assert len(db_customers) == 1
    assert db_customers[0].id == "zd_user_99"
    assert db_customers[0].source_system == "zendesk"
    assert db_customers[0].name == "Zendesk User"
    assert db_customers[0].email == "zd@example.com"
    session.close()
