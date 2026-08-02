from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from .models import Expense
from .storage import ExpenseStore

app = FastAPI(title="Smart Expense Tracker API", version="1.0.0")

_store = ExpenseStore()


def get_store() -> ExpenseStore:
    return _store


class TotalResponse(BaseModel):
    total: float
    category: Optional[str] = None


@app.post("/expenses", response_model=Expense, status_code=201)
def add_expense(expense: Expense, store: ExpenseStore = Depends(get_store)):
    if store.exists(expense.id):
        raise HTTPException(status_code=400, detail=f"Expense with id {expense.id} already exists")
    return store.add(expense)


@app.get("/expenses", response_model=List[Expense])
def view_expenses(store: ExpenseStore = Depends(get_store)):
    return store.get_all()

@app.get("/expenses/total", response_model=TotalResponse)
def get_overall_total(store: ExpenseStore = Depends(get_store)):
    return TotalResponse(total=round(store.total(), 2))


@app.get("/expenses/total/{category}", response_model=TotalResponse)
def get_total_by_category(category: str, store: ExpenseStore = Depends(get_store)):
    return TotalResponse(total=round(store.total_by_category(category), 2), category=category)


@app.get("/expenses/category/{category}", response_model=List[Expense])
def get_expenses_by_category(category: str, store: ExpenseStore = Depends(get_store)):
    filtered = store.get_by_category(category)
    if not filtered:
        raise HTTPException(status_code=404, detail=f"No expenses found for category '{category}'")
    return filtered


@app.delete("/expenses/{expense_id}", response_model=Expense)
def delete_expense(expense_id: int, store: ExpenseStore = Depends(get_store)):
    deleted = store.delete(expense_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")
    return deleted