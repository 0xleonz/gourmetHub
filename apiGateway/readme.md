### ¿Qué es un API Gateway?

Un **API Gateway** es un servidor que actúa como punto de entrada único para
gestionar, enrutar y procesar solicitudes de API entre clientes y
microservicios. Funciona como un "portero inteligente" que centraliza tareas
como:

1. **Enrutamiento**: Redirige solicitudes a los microservicios correctos.
2. **Autenticación/Autorización**: Valida tokens (JWT, OAuth).
3. **Limitación de tasa (Rate Limiting)**: Controla peticiones por segundo.
4. **Caché**: Almacena respuestas frecuentes.
5. **Transformación de datos**: Modifica formatos (JSON/XML).
6. **Balanceo de carga**: Distribuye tráfico entre instancias.
7. **Manejo de errores**: Centraliza respuestas de error.
8. **Logging y Monitoreo**: Registra métricas de uso.


#### 1. **API Gateway en Go** (`gateway/main.go`) ```go package main

import ( "log" "net/http" "net/http/httputil" "net/url")

// Proxy para los microservicios func newProxy(target string)
*httputil.ReverseProxy { url, _ := url.Parse(target) return
httputil.NewSingleHostReverseProxy(url) }

func main() { // Configurar proxies service1Proxy :=
newProxy("http://service1:8081") service2Proxy :=
newProxy("http://service2:8082")

// Enrutamiento http.HandleFunc("/service1/", func(w http.ResponseWriter, r
*http.Request) { service1Proxy.ServeHTTP(w, r) })

http.HandleFunc("/service2/", func(w http.ResponseWriter, r *http.Request) {
service2Proxy.ServeHTTP(w, r) })

// Health Check http.HandleFunc("/health", func(w http.ResponseWriter, r
*http.Request) { w.WriteHeader(http.StatusOK) w.Write([]byte("API Gateway está
activo")) })

log.Println("Gateway escuchando en :8080")
log.Fatal(http.ListenAndServe(":8080", nil)) } ```

---

#### 2. **Dockerfile para el Gateway** (`gateway/Dockerfile`) ```dockerfile FROM
golang:1.19-alpine

WORKDIR /app

COPY main.go .

RUN go build -o gateway .

EXPOSE 8080

CMD ["./gateway"] ```

---

#### 3. **Microservicios de Ejemplo** (`service1/Dockerfile` y
`service2/Dockerfile`) **service1/Dockerfile**: ```dockerfile FROM
python:3.9-slim

RUN pip install flask

WORKDIR /app

COPY service1.py .

CMD ["python", "service1.py"] ```

**service1/service1.py**: ```python from flask import Flask app =
Flask(__name__)

@app.route('/') def home(): return "Servicio 1: OK"

if __name__ == '__main__': app.run(host='0.0.0.0', port=8081) ```

> Repite similar para `service2` (cambia puerto y mensaje).

---

#### 4. **Docker Compose** (`docker-compose.yml`) ```yaml version: '3.8'

services: gateway: build: ./gateway ports:
- "8080:8080" depends_on:
- service1
- service2

  service1: build: ./service1 expose:
  - "8081"

  service2: build: ./service2 expose:
  - "8082" ```

---

#### 5. **Ejecutar el Sistema** ```bash docker-compose up --build ```

#### Probar Endpoints:
- **Gateway**: `http://localhost:8080/service1/`
- **Health Check**: `http://localhost:8080/health`

---

### Alternativa en Python (FastAPI) Si prefieres Python, usa **FastAPI** +
**Uvicorn**:

```python # gateway/main.py from fastapi import FastAPI, HTTPException from
httpx import AsyncClient

app = FastAPI() SERVICES = { "service1": "http://service1:8081", "service2":
                            "http://service2:8082" }

@app.get("/{service_name}/{path:path}") async def proxy_request(service_name:
                                                                str, path: str):
    if service_name not in SERVICES: raise HTTPException(status_code=404,
                                                         detail="Servicio no
                                                         encontrado")

    async with AsyncClient() as client: response = await
    client.get(f"{SERVICES[service_name]}/{path}") return response.json() ```

**Dockerfile**: ```dockerfile FROM python:3.9-slim

RUN pip install fastapi uvicorn httpx

WORKDIR /app

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] ```

---

### ¿Por qué usar un API Gateway?
- **Seguridad Centralizada**: Evita repetir lógica de autenticación en cada
servicio.
- **Simplicidad para Clientes**: Los clientes consumen un único endpoint.
- **Resiliencia**: Patrones como Circuit Breaker son fáciles de implementar.
- **Optimización**: Compresión, caché, y transformación en un solo lugar.

### Herramientas Profesionales (Alternativas)
- **Kong**: Basado en Nginx/OpenResty (Lua).
- **Apigee**: Plataforma empresarial de Google.
- **AWS API Gateway**: Servicio administrado en AWS.
- **Tyk**: Open-source con versión gratuita.

Este ejemplo básico en Go/Python + Docker es ideal para entender conceptos. En
producción, evalúa herramientas como **Kong** o soluciones cloud.
