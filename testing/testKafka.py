import requests
import time
import json
import threading
from kafka import KafkaConsumer

def test_kafka_consumer():
    print("\n=== Iniciando consumidor de prueba de Kafka ===")
    try:
        consumer = KafkaConsumer(
            'orders',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            consumer_timeout_ms=10000
        )
        
        print("✅ Consumidor Kafka conectado. Esperando mensajes...")
        for message in consumer:
            print(f"📥 Mensaje recibido: {message.value}")
            # Detener después de recibir un mensaje para la demo
            break
    except Exception as e:
        print(f"❌ Error en consumidor Kafka: {str(e)}")

def test_order_service():
    print("\n=== Probando servicio de órdenes ===")
    try:
        response = requests.post(
            "http://localhost:8080/order",
            json={
                "items": ["Pizza Trufa", "Agua Mineral"],
                "client": "Juan Pérez"
            },
            timeout=10
        )
        print(f"✅ Respuesta del servicio: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ Error probando servicio: {str(e)}")
        return False

def test_health_check():
    print("\n=== Probando health check ===")
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        print(f"✅ Health Check: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"❌ Health Check fallido: {str(e)}")

if __name__ == "__main__":
    print("=== Iniciando pruebas del sistema ===")
    
    # Iniciar consumidor en segundo plano
    kafka_thread = threading.Thread(target=test_kafka_consumer, daemon=True)
    kafka_thread.start()
    time.sleep(3)  # Esperar que el consumidor se conecte
    
    # Esperar que los servicios estén listos
    print("\n⏳ Esperando que los servicios se inicien (15 segundos)...")
    time.sleep(15)
    
    # Ejecutar pruebas
    if test_order_service():
        time.sleep(3)  # Dar tiempo a que llegue el mensaje a Kafka
    
    test_health_check()
    
    print("\nPruebas completadas. Manteniendo el consumidor activo por 20 segundos...")
    time.sleep(20)