from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    print(f"📦 Pedido recibido: {data}")
    return jsonify({
        "status": "success",
        "message": f"Pedido para {data.get('items', [])} creado",
        "order_id": "ORD-12345"
    }), 201

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "service": "order-service"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)