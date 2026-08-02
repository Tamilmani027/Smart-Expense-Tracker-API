import pytest
from fastapi.testclient import TestClient

from src.main import app, get_store
from src.storage import ExpenseStore


@pytest.fixture
def client():
    # Fresh store per test so tests don't leak state into each other.
    fresh_store = ExpenseStore()
    app.dependency_overrides[get_store] = lambda: fresh_store
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


SAMPLE = {"id": 1, "title": "Groceries", "amount": 42.5, "category": "Food", "date": "2026-08-01"}


def test_add_expense(client):
    r = client.post("/expenses", json=SAMPLE)
    assert r.status_code == 201
    assert r.json()["id"] == 1


def test_add_duplicate_expense_fails(client):
    client.post("/expenses", json=SAMPLE)
    r = client.post("/expenses", json=SAMPLE)
    assert r.status_code == 400


def test_add_expense_missing_field_fails(client):
    bad = {"title": "Groceries", "amount": 42.5, "category": "Food", "date": "2026-08-01"}
    r = client.post("/expenses", json=bad)
    assert r.status_code == 422


def test_add_expense_negative_amount_fails(client):
    bad = {**SAMPLE, "amount": -5}
    r = client.post("/expenses", json=bad)
    assert r.status_code == 422


def test_add_expense_blank_title_fails(client):
    bad = {**SAMPLE, "title": "   "}
    r = client.post("/expenses", json=bad)
    assert r.status_code == 422


def test_view_expenses_empty(client):
    r = client.get("/expenses")
    assert r.status_code == 200
    assert r.json() == []


def test_view_expenses(client):
    client.post("/expenses", json=SAMPLE)
    r = client.get("/expenses")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_filter_by_category(client):
    client.post("/expenses", json=SAMPLE)
    client.post("/expenses", json={**SAMPLE, "id": 2, "category": "Transport"})
    r = client.get("/expenses/category/Food")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["category"] == "Food"


def test_filter_by_category_case_insensitive(client):
    client.post("/expenses", json=SAMPLE)
    r = client.get("/expenses/category/food")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_filter_by_category_not_found(client):
    r = client.get("/expenses/category/Nonexistent")
    assert r.status_code == 404


def test_overall_total(client):
    client.post("/expenses", json=SAMPLE)
    client.post("/expenses", json={**SAMPLE, "id": 2, "amount": 10})
    r = client.get("/expenses/total")
    assert r.status_code == 200
    assert r.json()["total"] == 52.5


def test_total_by_category(client):
    client.post("/expenses", json=SAMPLE)
    client.post("/expenses", json={**SAMPLE, "id": 2, "category": "Transport", "amount": 10})
    r = client.get("/expenses/total/Food")
    assert r.status_code == 200
    assert r.json()["total"] == 42.5
    assert r.json()["category"] == "Food"


def test_delete_expense(client):
    client.post("/expenses", json=SAMPLE)
    r = client.delete("/expenses/1")
    assert r.status_code == 200
    assert client.get("/expenses").json() == []


def test_delete_nonexistent_expense(client):
    r = client.delete("/expenses/999")
    assert r.status_code == 404