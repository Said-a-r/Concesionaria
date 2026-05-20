from bson import ObjectId

def auto_to_dict(auto):
    """Convierte un documento de MongoDB a dict con _id como string"""
    if auto:
        auto['_id'] = str(auto['_id'])
    return auto

def crear_auto(db, datos):
    """Inserta un auto en la colección"""
    return db.autos.insert_one(datos)

def obtener_todos_autos(db):
    """Devuelve todos los autos"""
    """Ordenar por _id descendente para mostrar los más recientes primero"""
    autos = db.autos.find().sort('_id', -1)
    return [auto_to_dict(auto) for auto in autos]

def obtener_auto_por_id(db, auto_id):
    """Obtiene un auto por su ID"""
    try:
        auto = db.autos.find_one({'_id': ObjectId(auto_id)})
        return auto_to_dict(auto)
    except:
        return None

def actualizar_auto(db, auto_id, nuevos_datos):
    """Actualiza un auto"""
    db.autos.update_one(
        {'_id': ObjectId(auto_id)},
        {'$set': nuevos_datos}
    )

def eliminar_auto(db, auto_id):
    """Elimina un auto"""
    db.autos.delete_one({'_id': ObjectId(auto_id)})