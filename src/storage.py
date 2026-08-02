from typing import Dict, List, Optional
from .models import Expense


class ExpenseStore:
    def __init__(self) -> None:
        self._expenses: Dict[int, Expense] = {}

    def exists(self, expense_id: int) -> bool:
        return expense_id in self._expenses

    def add(self, expense: Expense) -> Expense:
        self._expenses[expense.id] = expense
        return expense

    def get_all(self) -> List[Expense]:
        return list(self._expenses.values())

    def get_by_category(self, category: str) -> List[Expense]:
        return [e for e in self._expenses.values() if e.category.lower() == category.lower()]

    def delete(self, expense_id: int) -> Optional[Expense]:
        return self._expenses.pop(expense_id, None)

    def total(self) -> float:
        return sum(e.amount for e in self._expenses.values())

    def total_by_category(self, category: str) -> float:
        return sum(e.amount for e in self._expenses.values() if e.category.lower() == category.lower())