from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URI')

# Mostrar solo los primeros 40 caracteres por seguridad
if uri:
    print(f"URI (parcial): {uri[:40]}...")
else:
    print("No se encontró MONGO_URI en el archivo .env")
    exit()

try:
    # Intentar conectar
    client = MongoClient(
        uri,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    
    # Hacer un ping para probar la conexión
    client.admin.command('ping')
    
    print("Conexión exitosa a MongoDB Atlas!")
    
    # Listar bases de datos
    dbs = client.list_database_names()
    print(f"Bases de datos disponibles: {dbs}")
    
except Exception as e:
    print(f"Error de conexión: {e}")