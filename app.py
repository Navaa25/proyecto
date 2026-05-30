from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
import certifi
import os

app = Flask(__name__)

# Conexión directa a tu base de datos real de MongoDB Atlas
MONGO_URI = "mongodb+srv://ajaviermonna5_user:250203ja@cluster0.ebicbgb.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client["Chedraui_Simulador"]
coleccion_ventas = db["ventas"] # Se guardará en una nueva colección llamada ventas

# Ruta para servir tu página web index.html de forma automática
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# API que recibe el JSON del Punto de Venta y lo manda a la nube
@app.route('/api/ventas', methods=['POST'])
def guardar_venta():
    try:
        datos_ticket = request.json
        if not datos_ticket:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Insertar el JSON directamente en MongoDB Atlas
        resultado = coleccion_ventas.insert_one(datos_ticket)
        return jsonify({"mensaje": "Venta guardada en la nube", "id": str(resultado.inserted_id)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Render nos asigna un puerto automático
    puerto = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=puerto)