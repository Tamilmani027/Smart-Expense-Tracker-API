from pydantic import BaseModel
from datetime import datetime


class Expense(BaseModel):
	id:int
	title:str
	amount:int
	category:str
	date:datetime

