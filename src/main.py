from fastapi import FastAPI

app=FastAPI()

expenses=[]

@app.post("/items")
def add_expenses():


