import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app, get_db
from models import Order

@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db

@pytest.fixture
def client(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_get_orders(client, mock_db):
    mock_order = Order(id=1, item_name="Keyboard", quantity=2)
    mock_db.query.return_value.all.return_value = [mock_order]

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "item_name": "Keyboard", "quantity": 2}]

def test_add_order(client, mock_db):
    def refresh_side_effect(order):
        order.id = 1

    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.side_effect = refresh_side_effect

    response = client.post("/", json={"item_name": "Mouse", "quantity": 5})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "item_name": "Mouse", "quantity": 5}
    assert mock_db.add.called
    assert mock_db.commit.called
    assert mock_db.refresh.called
