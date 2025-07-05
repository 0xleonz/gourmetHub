from fastapi import APIRouter
from app.models import ORDERS, RESERVATIONS, OrderStatus, ReservationStatus

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard():
    # Filtrar solo entidades no completadas
    queued_orders = [o for o in ORDERS if o.status != OrderStatus.done]
    queued_reservations = [r for r in RESERVATIONS if r.status != ReservationStatus.done]
    return {
        "orders": queued_orders,
        "reservations": queued_reservations
    }