import requests
import time

def test_system():
    # Probar servicio de órdenes
    order_response = requests.post(
        "http://localhost:8080/order",
        json={
            "items": ["Pizza Trufa", "Agua Mineral"],
            "client": "Juan Pérez"
        }
    )
    print("Respuesta de órdenes:", order_response.status_code, order_response.json())

    # Probar servicio de reservaciones
    reservation_response = requests.post(
        "http://localhost:8080/reservation",
        json={
            "name": "Ana García",
            "persons": 4,
            "time": "20:00"
        }
    )
    print("Respuesta de reservas:", reservation_response.status_code, reservation_response.json())

    # Probar health check
    health_response = requests.get("http://localhost:8080/health")
    print("Health Check:", health_response.status_code, health_response.text)

if __name__ == "__main__":
    time.sleep(2)  # Esperar que los servicios se inicien
    test_system()