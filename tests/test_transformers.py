import pytest
import datetime
from integrations.salesforce.transformer import SalesForceTransformer
from integrations.stripe.transformer import StripeTransformer
from models.unified import UnifiedCustomer, UnifiedTransaction
from integrations.stripe.models import StripeCustomerModel, StripeChargeModel

def test_salesforce_account_transform():
    raw_data = [
        {
            "Id": "001xyz",
            "Name": "Test Corp",
            "Type": "Customer",
            "CreatedDate": datetime.datetime(2023, 1, 1),
            "LastModifiedDate": datetime.datetime(2023, 1, 2)
        },
        {
            "Id": "002abc",
            "Name": None,  # Test null handling
            "Type": "Prospect",
            "CreatedDate": datetime.datetime(2023, 2, 1),
            "LastModifiedDate": datetime.datetime(2023, 2, 2)
        }
    ]
    
    transformer = SalesForceTransformer(record_type="account")
    result = transformer.transform(raw_data)
    
    assert len(result) == 2
    assert isinstance(result[0], UnifiedCustomer)
    assert result[0].id == "001xyz"
    assert result[0].source_system == "salesforce"
    assert result[0].name == "Test Corp"
    
    assert result[1].name == "Unknown"  # Null filled

def test_stripe_customer_transform():
    raw_data = [
        StripeCustomerModel(
            id="cus_123",
            object="customer",
            name="Jane Doe",
            email="jane@example.com",
            created=1672531200, # 2023-01-01
            balance=0
        ).model_dump()
    ]
    
    transformer = StripeTransformer(record_type="customer")
    result = transformer.transform(raw_data)
    
    assert len(result) == 1
    assert result[0].id == "cus_123"
    assert result[0].source_system == "stripe"
    assert result[0].name == "Jane Doe"
    assert result[0].email == "jane@example.com"
    assert result[0].created_at is not None

def test_stripe_charge_transform():
    raw_data = [
        StripeChargeModel(
            id="ch_123",
            object="charge",
            customer="cus_123",
            amount=1500, # 15.00
            currency="usd",
            paid=True,
            status="succeeded",
            created=1672531200
        ).model_dump()
    ]
    
    transformer = StripeTransformer(record_type="charge")
    result = transformer.transform(raw_data)
    
    assert len(result) == 1
    assert isinstance(result[0], UnifiedTransaction)
    assert result[0].id == "ch_123"
    assert result[0].amount == 15.0
    assert result[0].status == "succeeded"
    assert result[0].currency == "usd"

def test_zendesk_user_transform():
    from integrations.zendesk.transformer import ZenDeskTransformer
    raw_data = [
        {
            "id": "zd_user_1",
            "name": "Alex Smith",
            "email": "alex@zendesk.com",
            "phone": "987654321",
            "role": "agent",
            "active": True,
            "created_at": datetime.datetime(2023, 3, 1),
            "updated_at": datetime.datetime(2023, 3, 2)
        }
    ]
    transformer = ZenDeskTransformer()
    result = transformer.transform(raw_data)
    
    assert len(result) == 1
    assert isinstance(result[0], UnifiedCustomer)
    assert result[0].id == "zd_user_1"
    assert result[0].source_system == "zendesk"
    assert result[0].name == "Alex Smith"
    assert result[0].email == "alex@zendesk.com"


