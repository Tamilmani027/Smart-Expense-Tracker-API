from fastapi import FastAPI
from models import Expense
import HTTPException
app=FastAPI()

expenses=[]

@app.post("/expense/")
def add_expenses(expense: Expense):
    try:
        if expense.id in expenses:
            raise HTTPException(status_code=400, detail="Expense already exists")
        expenses[expense.id] = expense
        return {'message': 'expense added successfully', 'expense': expense}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
	



