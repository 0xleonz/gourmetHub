# app/routers/employees.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.kitchen.manager import list_employees, add_employee, delete_employee
from app.models import Employee
from pydantic import BaseModel

# router se pasa con /employees en 
router = APIRouter(tags=["employees"])

#lista de empleada serializada
@router.get("/", response_model=List[Employee])
async def get_employees():
    return list_employees()

class EmployeeIn(BaseModel):
    name: str
    capacity: int

@router.post("/", response_model=Employee, status_code=201)
async def create_employee(data: EmployeeIn):
    return add_employee(data.name, data.capacity)

@router.delete("/{emp_id}", status_code=204)
async def remove_employee(emp_id: int):
    if not delete_employee(emp_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return

