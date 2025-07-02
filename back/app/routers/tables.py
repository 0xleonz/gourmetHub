from fastapi import APIRouter, HTTPException
from typing import List
from app.kitchen.manager import list_tables, add_table, delete_table
from app.models import Table
from pydantic import BaseModel

router = APIRouter(tags=["tables"])

@router.get("/", response_model=List[Table])
async def get_tables():
    return list_tables()

class TableIn(BaseModel):
    capacity: int

@router.post("/", response_model=Table, status_code=201)
async def create_table(data: TableIn):
    return add_table(data.capacity)

@router.delete("/{table_id}", status_code=204)
async def remove_table(table_id: int):
    if not delete_table(table_id):
        raise HTTPException(status_code=404, detail="Table not found")
    return

