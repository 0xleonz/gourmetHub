# app/kitchen/prepare.py
import threading
import time
from datetime import datetime, timedelta
from typing import Optional

from app.models import (
    ORDERS, EMPLOYEES, MENU_ITEMS,
    ReservationStatus, OrderStatus
)

CYCLE_INTERVAL = 5  # segundos entre cada ciclo de despacho

# Que hace esto
def run_cycle():
    """
    Ciclo que corre en background: asigna órdenes, actualiza estados y libera empleados.
    """
    while True:
        now = datetime.utcnow()
        # 1) Liberar empleados de órdenes completadas
        for order in ORDERS:
            if order.status == OrderStatus.preparing and order.done_at and now >= order.done_at:
                # liberar slot
                emp = next((e for e in EMPLOYEES if e.id == order.assigned_employee), None)
                if emp:
                    emp.busy_slots = max(0, emp.busy_slots - 1)
                order.status = OrderStatus.done

        # 2) Asignar nuevas órdenes
        for order in ORDERS:
            if order.status != OrderStatus.queued:
                continue
            # buscar empleado con slot libre
            emp = next((e for e in EMPLOYEES if e.busy_slots < e.capacity), None)
            if not emp:
                break  # no hay más capacidad ahora
            # asignar
            order.assigned_employee = emp.id
            order.status = OrderStatus.preparing
            order.started_at = now
            # calcular tiempo total de prep
            total_prep = sum(
                next((m.prep_time for m in MENU_ITEMS if m.id == item_id), 0)
                for item_id in order.items
            )
            order.done_at = now + timedelta(seconds=total_prep)
            emp.busy_slots += 1

        time.sleep(CYCLE_INTERVAL)

# Que hace esto
def start_background_thread():
    thread = threading.Thread(target=run_cycle, daemon=True)
    thread.start()

# Que hace esto
def get_order_eta(order_id: int) -> Optional[int]:
    """
    Retorna ETA en segundos para la orden o None si no existe.
    """
    order = next((o for o in ORDERS if o.id == order_id), None)
    if not order:
        return None
    now = datetime.utcnow()
    if order.status == OrderStatus.done:
        return 0
    if order.status == OrderStatus.preparing and order.done_at:
        return max(0, int((order.done_at - now).total_seconds()))
    # si está en cola, estimamos sumando todos los prep_times pendientes y dividiendo
    pending = [o for o in ORDERS if o.status == OrderStatus.queued or o.status == OrderStatus.preparing]
    total_seconds = sum(
        sum(next((m.prep_time for m in MENU_ITEMS if m.id == item), 0) for item in o.items)
        for o in pending
    )
    total_capacity = sum(e.capacity - e.busy_slots for e in EMPLOYEES)
    if total_capacity <= 0:
        return None
    return int(total_seconds / total_capacity)

# Que hace esto
def get_reservation_eta(res_id: int) -> Optional[int]:
    """
    Retorna ETA en segundos para la reserva o None si no existe.
    Estima 5 min por cada reserva en cola antes de la tuya.
    """
    res = next((r for r in RESERVATIONS if r.id == res_id), None)
    if not res:
        return None
    now = datetime.utcnow()
    if res.status in (ReservationStatus.seated, ReservationStatus.done):
        return 0
    # contamos cuántas reservas en cola llegaron antes que la tuya
    queued = sorted(
        [r for r in RESERVATIONS if r.status == ReservationStatus.queued],
        key=lambda r: r.created_at
    )
    # posición en cola (0-based)
    idx = next((i for i, r in enumerate(queued) if r.id == res_id), None)
    if idx is None:
        return None
    # asumimos 300 s por reserva
    return idx * 300
