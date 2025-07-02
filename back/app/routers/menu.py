# app/routers/menu.py
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from app.kitchen.manager import (
    list_menu_items, add_menu_item, update_menu_item, delete_menu_item
)
from app.models import MenuItem

router = APIRouter(tags=["menu"])

@router.get("/", response_model=List[MenuItem])
async def get_menu():
    return list_menu_items()

class MenuItemIn(BaseModel):
    name: str
    prep_time: int

# Que hace esto
@router.post("/", response_model=MenuItem, status_code=201)
async def create_menu_item(item: MenuItemIn):
    return add_menu_item(item.name, item.prep_time)

# Que hace esto
@router.put("/{item_id}", response_model=MenuItem)
async def modify_menu_item(item_id: int, item: MenuItemIn):
    updated = update_menu_item(item_id, item.name, item.prep_time)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated

# Que hace esto
@router.delete("/{item_id}", status_code=204)
async def remove_menu_item(item_id: int):
    if not delete_menu_item(item_id):
        raise HTTPException(status_code=404, detail="Menu item not found")
    return

