import pytest
from fastapi.testclient import TestClient
# pyrefly: ignore [missing-import]
from sqlalchemy import create_engine
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import sessionmaker
import os   

# Set custom database URL before imports
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from database import Base, get_db
from main import app

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    # Clean database before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def test_create_product():
    response = client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 99.99, "quantity": 10}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["sku"] == "PROD001"
    assert data["price"] == "99.99"
    assert data["quantity"] == 10

def test_duplicate_sku():
    # Create first product
    client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 99.99, "quantity": 10}
    )
    # Attempt second with duplicate SKU
    response = client.post(
        "/products",
        json={"name": "Test Product 2", "sku": "PROD001", "price": 49.99, "quantity": 5}
    )
    assert response.status_code == 400
    assert "SKU already exists" in response.json()["detail"]

def test_invalid_product_data():
    # Negative quantity
    response = client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 99.99, "quantity": -5}
    )
    assert response.status_code == 422

    # Negative/zero price
    response = client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 0, "quantity": 10}
    )
    assert response.status_code == 422

def test_create_customer():
    response = client.post(
        "/customers",
        json={"name": "John Doe", "email": "john@example.com", "phone": "1234567890"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_duplicate_customer_email():
    client.post(
        "/customers",
        json={"name": "John Doe", "email": "john@example.com", "phone": "1234567890"}
    )
    response = client.post(
        "/customers",
        json={"name": "Jane Doe", "email": "john@example.com", "phone": "0987654321"}
    )
    assert response.status_code == 400
    assert "email already registered" in response.json()["detail"]

def test_create_order_and_deduct_inventory():
    # 1. Setup product & customer
    prod_resp = client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 100.00, "quantity": 10}
    )
    prod_id = prod_resp.json()["id"]

    cust_resp = client.post(
        "/customers",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    cust_id = cust_resp.json()["id"]

    # 2. Place Order
    order_resp = client.post(
        "/orders",
        json={
            "customer_id": cust_id,
            "items": [{"product_id": prod_id, "quantity": 3}]
        }
    )
    assert order_resp.status_code == 201
    order_data = order_resp.json()
    assert order_data["total_amount"] == "300.00"
    
    # 3. Check updated product quantity
    get_prod = client.get(f"/products/{prod_id}")
    assert get_prod.json()["quantity"] == 7

def test_insufficient_inventory():
    # Setup product & customer
    prod_resp = client.post(
        "/products",
        json={"name": "Test Product", "sku": "PROD001", "price": 10.00, "quantity": 2}
    )
    prod_id = prod_resp.json()["id"]

    cust_resp = client.post(
        "/customers",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    cust_id = cust_resp.json()["id"]

    # Order more than available quantity
    order_resp = client.post(
        "/orders",
        json={
            "customer_id": cust_id,
            "items": [{"product_id": prod_id, "quantity": 3}]
        }
    )
    assert order_resp.status_code == 400
    assert "Insufficient inventory" in order_resp.json()["detail"]

    # Verify inventory was NOT deducted
    get_prod = client.get(f"/products/{prod_id}")
    assert get_prod.json()["quantity"] == 2
