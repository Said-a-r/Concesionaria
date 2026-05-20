from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv('MONGO_URI')


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
    
   
    client.admin.command('ping')
    
    print("Conexión exitosa a MongoDB Atlas!")
    
    
    dbs = client.list_database_names()
    print(f"Bases de datos disponibles: {dbs}")
    
except Exception as e:
    print(f"Error de conexión: {e}")