# app/routers/orders.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.kitchen.prepare import get_order_eta
from app.kitchen.manager import list_menu_items
from app.models import Order, ORDERS, MENU_ITEMS, OrderStatus

# 1) Define y exporta el router
router = APIRouter(tags=["orders"])

# 2) Input schema
class OrderIn(BaseModel):
    items: List[int]

# Que hace esto
# 3) Endpoints
@router.post("", response_model=Order, status_code=201)
async def create_order(order: OrderIn):
    # lógica para crear la orden...
    new_id = max((o.id for o in ORDERS), default=0) + 1
    o = Order(id=new_id, items=order.items)
    ORDERS.append(o)
    return o

# Que hace esto
@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: int):
    o = next((o for o in ORDERS if o.id == order_id), None)
    if not o:
        raise HTTPException(404, "Order not found")
    # añade un campo ETA dinámico
    eta = get_order_eta(order_id)
    return o.copy(update={"eta": eta})

# Que hace esto
@router.get("", response_model=List[Order])
async def list_orders():
    return ORDERS

