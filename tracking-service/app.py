# tracking_service/app.py
from flask import Flask, render_template
from kafka import KafkaConsumer
import threading
import json
import time

app = Flask(__name__)

# Configuración de mesas (ejemplo: 5 mesas con capacidades [2, 4, 4, 6, 8])
TABLES = [
    {"id": 1, "capacity": 2, "status": "libre", "reservation_id": None},
    {"id": 2, "capacity": 4, "status": "libre", "reservation_id": None},
    {"id": 3, "capacity": 4, "status": "libre", "reservation_id": None},
    {"id": 4, "capacity": 6, "status": "libre", "reservation_id": None},
    {"id": 5, "capacity": 8, "status": "libre", "reservation_id": None}
]

orders = []
reservations_queue = []
reservations_active = []

def consume_kafka():
    consumer = KafkaConsumer(
        'orders',
        'reservations',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    
    for message in consumer:
        if message.topic == 'orders':
            orders.append(message.value)
            print(f"Orden recibida: {message.value}")
        
        elif message.topic == 'reservations':
            new_reservation = message.value
            reservations_queue.append(new_reservation)
            print(f"Reserva recibida: {new_reservation}")
            assign_table()

def assign_table():
    global reservations_queue, TABLES
    
    for reservation in reservations_queue[:]:
        for table in TABLES:
            if table['status'] == 'libre' and table['capacity'] >= reservation['people']:
                # Asignar mesa
                table['status'] = 'ocupada'
                table['reservation_id'] = reservation['id']
                reservations_active.append(reservation)
                reservations_queue.remove(reservation)
                
                # Programar liberación (ej: después de 2 horas)
                release_time = time.time() + 7200  # Debug: 10 segundos
                threading.Thread(
                    target=release_table,
                    args=(table['id'], reservation['id'], release_time),
                    daemon=True
                ).start()
                print(f"Mesa {table['id']} asignada a reserva {reservation['id']}")
                break

def release_table(table_id, reservation_id, release_time):
    time.sleep(max(0, release_time - time.time()))
    
    for table in TABLES:
        if table['id'] == table_id:
            table['status'] = 'libre'
            table['reservation_id'] = None
            print(f"Mesa {table_id} liberada")
    
    # Eliminar reserva activa
    for r in reservations_active[:]:
        if r['id'] == reservation_id:
            reservations_active.remove(r)
    
    # Asignar siguiente reserva
    assign_table()

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                           orders=orders,
                           tables=TABLES,
                           queue=reservations_queue,
                           active=reservations_active)

if __name__ == '__main__':
    threading.Thread(target=consume_kafka, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)