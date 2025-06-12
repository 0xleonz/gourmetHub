from flask import Flask, jsonify, request
from kafka import KafkaProducer
import json
import os
import uuid
import logging
import time
import socket

app = Flask(__name__)

# Configuración de Kafka
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:29092')
TOPIC_NAME = os.getenv('KAFKA_TOPIC', 'orders')

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Mejorar la resolución de DNS para Docker
def resolve_host(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        logger.warning(f"⚠️ No se pudo resolver {hostname}")
        return hostname

# Intento de conexión a Kafka con reintentos mejorados
def create_producer(max_retries=15, retry_delay=7):
    resolved_broker = resolve_host(KAFKA_BROKER.split(':')[0])
    full_broker = f"{resolved_broker}:{KAFKA_BROKER.split(':')[1]}"
    logger.info(f"🔧 Intentando conectar a Kafka en: {full_broker}")
    
    for attempt in range(max_retries):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[full_broker],
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 11, 5),
                request_timeout_ms=15000,
                security_protocol='PLAINTEXT'
            )
            # Prueba de conexión
            producer.send(TOPIC_NAME, value={'test': 'connection_check'})
            producer.flush(timeout=10)
            logger.info(f"✅ Conectado a Kafka en {full_broker} (Intento {attempt+1}/{max_retries})")
            return producer
        except Exception as e:
            logger.error(f"❌ Intento {attempt+1}/{max_retries}: Error conectando a Kafka - {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"⏳ Reintentando en {retry_delay} segundos...")
                time.sleep(retry_delay)
    logger.critical("🚨 No se pudo conectar a Kafka después de todos los reintentos")
    return None

producer = create_producer()

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    logger.info(f"📦 Pedido recibido: {data}")
    
    # Generar ID de orden único
    order_id = f"ORD-{str(uuid.uuid4())[:8]}"
    
    # Crear mensaje para Kafka
    kafka_message = {
        "order_id": order_id,
        "items": data.get('items', []),
        "client": data.get('client', ''),
        "status": "CREATED",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "service": "order-service"
    }
    
    # Publicar en Kafka si el productor está disponible
    if producer:
        try:
            producer.send(TOPIC_NAME, value=kafka_message)
            # No hacer flush inmediato para mejor rendimiento
            logger.info(f"🚀 Evento enviado a Kafka (topic: {TOPIC_NAME}): {kafka_message}")
        except Exception as e:
            logger.error(f"⚠️ Error publicando en Kafka: {str(e)}")
    else:
        logger.warning("Kafka producer no disponible, omitiendo publicación")
    
    return jsonify({
        "status": "success",
        "message": f"Pedido para {data.get('items', [])} creado",
        "order_id": order_id,
        "kafka_status": "published" if producer else "disabled"
    }), 201

@app.route('/health', methods=['GET'])
def health_check():
    kafka_status = "connected" if (producer and not producer._closed) else "disconnected"
    return jsonify({
        "status": "ok",
        "service": "order-service",
        "kafka": kafka_status,
        "broker": KAFKA_BROKER,
        "topic": TOPIC_NAME
    }), 200

if __name__ == '__main__':
    logger.info("🚀 Iniciando Order Service...")
    app.run(host='0.0.0.0', port=8080)