# 🍽️ GourmetHub - Sistema de Gestión de Restaurante en Tiempo Real

[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Docker](https://img.shields.io/badge/Docker-Containers-blue)
![Microservicios](https://img.shields.io/badge/Architecture-Microservices-green)
![RabbitMQ](https://img.shields.io/badge/Apache_rabbitMQ-Streaming-orange)

**GourmetHub** es un sistema de gestión de restaurante basado en microservicios
que procesa órdenes y reservaciones en tiempo real usando RabbitMQ. Diseñado
para alta escalabilidad y seguimiento de métricas de desempeño.

graph LR
    A[Cliente] --> C[Order Service]
    A[Cliente] --> D[Reservation Service]
    C -->|Publica| K[rabbitMQ]
    D -->|Publica| K[rabbitMQ]
    K -->|Consume| E[Tracking Service]
    E --> G[Dashboard]
    H[Simulator] --> C
    H[Simulator] --> D

<!-- El api gateway implementa un reverse proxy, -->
