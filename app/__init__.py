from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave-temporal-cambiar-despues'
    
    # Configuración de MongoDB Atlas
    mongo_uri = os.getenv('MONGO_URI')
    db_name = os.getenv('DB_NAME')
    
    # Conectar con opciones para Atlas
    client = MongoClient(
        mongo_uri,
        tlsAllowInvalidCertificates=True  # Importante para evitar errores SSL
    )
    app.db = client[db_name]
    
    # Configuración de imágenes
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['DEFAULT_IMAGE'] = '/static/default_car.jpg'
    
    # Registrar rutas
    from app.routes.autos_routes import autos_bp
    app.register_blueprint(autos_bp)
    
    return app