import threading
import time
from datetime import datetime, timedelta

from app.models import (
    ORDERS, OrderStatus,
    RESERVATIONS, ReservationStatus,
    MENU_ITEMS, EMPLOYEES, TABLES
)

def process_orders():
    for order in ORDERS:
        if order.status == OrderStatus.queued:
            emp = next((e for e in EMPLOYEES if e.busy_slots < e.capacity), None)
            if not emp:
                continue
            emp.busy_slots += 1
            order.assigned_employee = emp.id
            order.status = OrderStatus.preparing
            order.started_at = datetime.utcnow()
            total = sum(
                next(mi.prep_time for mi in MENU_ITEMS if mi.id == item_id)
                for item_id in order.items
            )
            order.eta = total
        elif order.status == OrderStatus.preparing:
            elapsed = (datetime.utcnow() - order.started_at).total_seconds()
            if elapsed >= order.eta:
                order.status = OrderStatus.done
                order.done_at = datetime.utcnow()
                emp = next(e for e in EMPLOYEES if e.id == order.assigned_employee)
                emp.busy_slots -= 1

def process_reservations():
    for res in RESERVATIONS:
        if res.status == ReservationStatus.queued:
            assigned = []
            needed = res.party_size
            for t in TABLES:
                if t.reserved_until is None and needed > 0:
                    assigned.append(t.id)
                    t.reserved_until = datetime.utcnow() + timedelta(seconds=30)
                    needed -= t.capacity
            if needed > 0:
                continue
            res.tables_assigned = assigned
            res.status = ReservationStatus.seated
            res.seated_at = datetime.utcnow()
            res.eta = 30
        elif res.status == ReservationStatus.seated:
            elapsed = (datetime.utcnow() - res.seated_at).total_seconds()
            if elapsed >= res.eta:
                res.status = ReservationStatus.done
                res.done_at = datetime.utcnow()
                for t in TABLES:
                    if t.id in res.tables_assigned:
                        t.reserved_until = None

def worker_loop():
    while True:
        process_orders()
        process_reservations()
        time.sleep(1)

def start_background_thread():
    t = threading.Thread(target=worker_loop, daemon=True)
    t.start()

def get_order_eta(order_id: int) -> int:
    o = next((o for o in ORDERS if o.id == order_id), None)
    if not o or o.status != OrderStatus.preparing:
        return 0
    elapsed = (datetime.utcnow() - o.started_at).total_seconds()
    return max(0, o.eta - int(elapsed))

def get_reservation_eta(res_id: int) -> int:
    r = next((r for r in RESERVATIONS if r.id == res_id), None)
    if not r or r.status != ReservationStatus.seated:
        return 0
