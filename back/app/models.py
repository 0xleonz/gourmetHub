# app/models.py
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


# Limitamos las opciones :)
# ——— Enums ———
class OrderStatus(str, Enum):
    queued = "queued"
    preparing = "preparing"
    done = "done"

class ReservationStatus(str, Enum):
    queued = "queued"
    seated = "seated"
    done = "done"

# ——— Modelos ———
class MenuItem(BaseModel):
    id: int
    name: str
    prep_time: int#En segundos

class Employee(BaseModel):
    id: int
    name: str
    capacity: int # slots totales
    busy_slots: int = 0  # slots ocupados delete??

class Table(BaseModel):
    id: int
    capacity: int
    reserved_until: Optional[datetime] = None

class Order(BaseModel):
    id: int
    items: List[int] # IDs de MenuItem
    created_at: datetime = datetime.utcnow()
    status: OrderStatus = OrderStatus.queued
    assigned_employee: Optional[int] = None
    started_at: Optional[datetime] = None
    done_at: Optional[datetime] = None
    eta: Optional[int] = None

class Reservation(BaseModel):
    id: int
    name: str
    party_size: int
    created_at: datetime = datetime.utcnow()
    status: ReservationStatus = ReservationStatus.queued
    tables_assigned: List[int] = []
    seated_at: Optional[datetime] = None
    done_at: Optional[datetime] = None
    eta: Optional[int] = None

# ——— Stores en memoria ———
MENU_ITEMS: List[MenuItem] = []
EMPLOYEES: List[Employee] = []
TABLES: List[Table] = []
ORDERS: List[Order] = []
RESERVATIONS: List[Reservation] = []

