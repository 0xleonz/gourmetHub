# app/main.py
from fastapi import FastAPI
from app.routers import (
    orders, reservations,
    menu, employees, tables,
    dashboard  # maybe, should add it??
)
from app.kitchen.prepare import start_background_thread

app = FastAPI(title="GourmetHub MVP")

# Arranca kitcherina para procesar ordenes
# reservas y para procesarlos
start_background_thread()

# Routers públicos:
#
# Routers proteghidos
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
app.include_router(menu.router)
app.include_router(employees.router)
app.include_router(tables.router)

@app.get("/")
async def root():
    return {"message": "just testing xd"}

if __name__ == "__main__":
    print("Arrancando GourmetHub API en 8000")
    import uvicorn
    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=8000,
                reload=True)

