from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/reservation', methods=['POST'])
def create_reservation():
    data = request.json
    print(f"🍽️ Reserva recibida: {data}")
    return jsonify({
        "status": "success",
        "message": f"Reserva para {data.get('name', '')} creada",
        "reservation_id": "RES-67890"
    }), 201

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "reservation-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)