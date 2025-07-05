# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import orders, reservations, menu, employees, tables, dashboard
from app.kitchen.prepare import start_background_thread

app = FastAPI(title="GourmetHub MVP")

# 1) CORS para tu frontend Svelte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2) Inicia el ciclo de la cocina
start_background_thread()

# 3) Routers públicos y protegidos
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
app.include_router(menu.router)
app.include_router(employees.router)
app.include_router(tables.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    return {"message": "just testing xd"}

if __name__ == "__main__":
    print("🚀 Arrancando GourmetHub API en 8000")
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
