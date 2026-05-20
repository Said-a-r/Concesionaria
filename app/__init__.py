from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
from flask import Flask, render_template
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave-temporal-cambiar-despues'
    
    
    mongo_uri = os.getenv('MONGO_URI')
    db_name = os.getenv('DB_NAME')
    
    
    client = MongoClient(
        mongo_uri,
        tlsAllowInvalidCertificates=True 
    )
    app.db = client[db_name]
    
    # Configuración de imágenes
    app.config['UPLOAD_FOLDER'] = os.path.join('app', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['DEFAULT_IMAGE'] = '/static/uploads/default.jpg'
    
    
    from app.routes.autos_routes import autos_bp
    app.register_blueprint(autos_bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')

    return app