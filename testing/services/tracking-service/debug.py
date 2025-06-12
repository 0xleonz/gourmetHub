# testing/services/tracking-service/debug.py
from kafka import KafkaProducer
import random
import time
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

customers = ["Ana", "Luis", "Carlos", "Marta", "Jorge", "Elena"]
menu_items = ["Pizza", "Pasta", "Ensalada", "Sopa", "Postre", "Bebida"]

order_id = 1
reservation_id = 1

try:
    while True:
        # Generar orden aleatoria
        producer.send('orders', {
            'id': order_id,
            'items': random.sample(menu_items, random.randint(1, 3)),
            'timestamp': int(time.time())
        })
        order_id += 1
        
        # Generar reserva aleatoria (cada 5 segundos)
        if random.random() > 0.7:
            producer.send('reservations', {
                'id': reservation_id,
                'customer': random.choice(customers),
                'people': random.choice([2, 2, 4, 4, 6, 8]),
                'timestamp': int(time.time())
            })
            reservation_id += 1
        
        time.sleep(random.uniform(0.5, 2))

except KeyboardInterrupt:
    print("Simulación detenida")