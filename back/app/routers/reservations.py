# app/routers/reservations.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.kitchen.prepare import get_reservation_eta
from app.models import Reservation, RESERVATIONS

router = APIRouter(tags=["reservations"])

class ReservationIn(BaseModel):
    name: str
    party_size: int

@router.post("", response_model=Reservation, status_code=201)
async def create_reservation(res: ReservationIn):
    new_id = max((r.id for r in RESERVATIONS), default=0) + 1
    r = Reservation(id=new_id, name=res.name, party_size=res.party_size)
    RESERVATIONS.append(r)
    return r

@router.get("/{res_id}", response_model=Reservation)
async def get_reservation(res_id: int):
    r = next((r for r in RESERVATIONS if r.id == res_id), None)
    if not r:
        raise HTTPException(404, "Reservation not found")
    eta = get_reservation_eta(res_id)
    return r.copy(update={"eta": eta})

@router.get("", response_model=List[Reservation])
async def list_reservations():
    return RESERVATIONS

