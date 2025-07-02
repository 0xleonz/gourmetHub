# app/kitchen/manager.py
# Basicamente CRUDS para MENU_ITEMS, EMPLOYEES y TABLES
from datetime import datetime
from typing import List, Optional

from app.models import (
    MENU_ITEMS, EMPLOYEES, TABLES,
    MenuItem, Employee, Table
)

# ——— Menú ——— un CRUD basico
# Que hace esto
def list_menu_items() -> List[MenuItem]:
    return MENU_ITEMS

# agrega un id creciente que agrega a lo que tenemos en
# el "menu"
def add_menu_item(name: str, prep_time: int) -> MenuItem:
    new_id = max((m.id for m in MENU_ITEMS), default=0) + 1
    item = MenuItem(id=new_id, name=name, prep_time=prep_time)
    MENU_ITEMS.append(item)
    return item

# Para modificar un item del menu
def update_menu_item(item_id: int, name: Optional[str], prep_time: Optional[int]) -> Optional[MenuItem]:
    item = next((m for m in MENU_ITEMS if m.id == item_id), None)
    if not item:
        return None
    if name is not None:
        item.name = name
    if prep_time is not None:
        item.prep_time = prep_time
    return item

# Borra del menu
def delete_menu_item(item_id: int) -> bool:
    global MENU_ITEMS
    before = len(MENU_ITEMS)
    MENU_ITEMS[:] = [m for m in MENU_ITEMS if m.id != item_id]
    return len(MENU_ITEMS) < before

# ——— Empleados ———
def list_employees() -> List[Employee]:
    return EMPLOYEES

def add_employee(name: str, capacity: int) -> Employee:
    new_id = max((e.id for e in EMPLOYEES), default=0) + 1
    emp = Employee(id=new_id, name=name, capacity=capacity)
    EMPLOYEES.append(emp)
    return emp

def delete_employee(emp_id: int) -> bool:
    global EMPLOYEES
    before = len(EMPLOYEES)
    EMPLOYEES[:] = [e for e in EMPLOYEES if e.id != emp_id]
    return len(EMPLOYEES) < before

# ——— Mesas ———
def list_tables() -> List[Table]:
    return TABLES

def add_table(capacity: int) -> Table:
    new_id = max((t.id for t in TABLES), default=0) + 1
    table = Table(id=new_id, capacity=capacity)
    TABLES.append(table)
    return table

def delete_table(table_id: int) -> bool:
    global TABLES
    before = len(TABLES)
    TABLES[:] = [t for t in TABLES if t.id != table_id]
    return len(TABLES) < before
