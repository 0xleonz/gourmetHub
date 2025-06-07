# 🍽️ GourmetHub - Sistema de Gestión de Restaurante en Tiempo Real

[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Docker](https://img.shields.io/badge/Docker-Containers-blue)
![Microservicios](https://img.shields.io/badge/Architecture-Microservices-green)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-Streaming-orange)

**GourmetHub** es un sistema de gestión de restaurante basado en microservicios
que procesa órdenes y reservaciones en tiempo real usando Apache Kafka. Diseñado
para alta escalabilidad y seguimiento de métricas de desempeño.

```mermaid
graph LR
    A[Cliente] --> B[API Gateway]
    B -->|Publica| C[Kafka]
    C --> D[Order Service]
    C --> E[Reservation Service]
    D --> F[Tracking Service]
    E --> F
    F --> G[Dashboard]
    H[Simulator] --> C
```

