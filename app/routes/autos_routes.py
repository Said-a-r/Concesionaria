from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.auto_model import crear_auto, obtener_todos_autos, obtener_auto_por_id, actualizar_auto, eliminar_auto
import os
from werkzeug.utils import secure_filename
from datetime import datetime

autos_bp = Blueprint('autos', __name__, url_prefix='/autos')

def allowed_file(filename):
    """Verifica si el archivo tiene extensión permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def guardar_imagen(archivo):
    """Guarda la imagen y retorna la URL. Si falla, retorna None"""
    if archivo and archivo.filename != '' and allowed_file(archivo.filename):
        nombre_seguro = secure_filename(archivo.filename)
        nombre_unico = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nombre_seguro}"
        ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_unico)
        
        
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        archivo.save(ruta_guardado)
        return f"/static/uploads/{nombre_unico}"
    return None

@autos_bp.route('/')
def lista():
    categoria = request.args.get('categoria', '').strip()

    busqueda = request.args.get('buscar', '').strip()

    precio_rango = request.args.get('precio_rango', '').strip()
    print("PRECIO:", precio_rango)
    
    # Construir filtro de MongoDB
    filtro = {}
    
    # Filtro por categoría (exacto)
    if categoria:
        filtro['categoria'] = categoria
    
    # Filtro por búsqueda (marca o modelo, case-insensitive)
    if busqueda:
        filtro['$or'] = [
            {'marca': {'$regex': busqueda, '$options': 'i'}},
            {'modelo': {'$regex': busqueda, '$options': 'i'}}
        ]
      # FILTRO PRECIO
    if precio_rango == "0-30000":
        filtro['precio'] = {'$lt': 30000}

    elif precio_rango == "30000-70000":
        filtro['precio'] = {
            '$gte': 30000,
            '$lte': 70000
        }

    elif precio_rango == "70000-100000":
        filtro['precio'] = {
            '$gte': 70000,
            '$lte': 100000
        }

    elif precio_rango == "100000-150000":
        filtro['precio'] = {
            '$gte': 100000,
            '$lte': 150000
        }

    elif precio_rango == "150000+":
        filtro['precio'] = {'$gt': 150000}

    elif precio_rango == "Menor":
        autos_cursor = current_app.db.autos.find(filtro).sort('precio', 1)

    elif precio_rango == "Mayor":
        autos_cursor = current_app.db.autos.find(filtro).sort('precio', -1)

    # SI NO ES MENOR O MAYOR
    if precio_rango not in ["Menor", "Mayor"]:
        autos_cursor = current_app.db.autos.find(filtro).sort('_id', -1)

    autos = []

    for auto in autos_cursor:
        auto['_id'] = str(auto['_id'])
        autos.append(auto)

    return render_template(
        'autos/lista.html',
        autos=autos,
        categoria_actual=categoria
    )

    # Aplicar filtro en MongoDB
    if filtro:
        autos_cursor = current_app.db.autos.find(filtro).sort('_id', -1)
    else:
        autos_cursor = current_app.db.autos.find().sort('_id', -1)
    
    # Convertir ObjectId a string
    autos = []
    for auto in autos_cursor:
        print("AUTO ENCONTRADO:", auto.get('precio'))

    auto['_id'] = str(auto['_id'])
    autos.append(auto)
    
    return render_template(
        'autos/lista.html',
        autos=autos,
        categoria_actual=categoria
    )

@autos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            # obtener datos del formulario
            datos = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'),
                'año': int(request.form.get('año')),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria': request.form.get('categoria'),
                'imagen_url': current_app.config['DEFAULT_IMAGE']
            }
            
            # 2. validaciones básicas
            if not datos['marca'] or not datos['modelo']:
                flash('Marca y modelo son obligatorios', 'danger')
                return render_template('autos/nuevo.html')
            
            if datos['año'] < 1900 or datos['año'] > 2026:
                flash('Año inválido (debe ser entre 1900 y 2026)', 'danger')
                return render_template('autos/nuevo.html')
            
            if datos['precio'] <= 0:
                flash('El precio debe ser mayor a 0', 'danger')
                return render_template('autos/nuevo.html')
            
            if datos['stock'] < 0:
                flash('El stock no puede ser negativo', 'danger')
                return render_template('autos/nuevo.html')
            
            
            if 'imagen' in request.files:
                imagen_url = guardar_imagen(request.files['imagen'])
                if imagen_url:
                    datos['imagen_url'] = imagen_url
            
            # 4. Guardar en MongoDB
            crear_auto(current_app.db, datos)
            
            flash(f'Auto {datos["marca"]} {datos["modelo"]} creado exitosamente', 'success')
            return redirect(url_for('autos.lista'))
            
        except Exception as e:
            flash(f'Error al crear el auto: {str(e)}', 'danger')
    
    return render_template('autos/nuevo.html')

@autos_bp.route('/<id>')
def detalle(id):
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    return render_template('autos/detalle.html', auto=auto)

@autos_bp.route('/<id>/editar', methods=['GET', 'POST'])
def editar(id):
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    
    if request.method == 'POST':
        try:
            datos = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'),
                'año': int(request.form.get('año')),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria': request.form.get('categoria'),
            }
            
            # Mantener imagen o mantener
            datos['imagen_url'] = auto.get('imagen_url')
            if 'imagen' in request.files:
                imagen_url = guardar_imagen(request.files['imagen'])
                if imagen_url:
                    datos['imagen_url'] = imagen_url
            
            actualizar_auto(current_app.db, id, datos)
            flash('Auto actualizado exitosamente', 'success')
            return redirect(url_for('autos.lista'))
        except Exception as e:
            flash(f'Error al actualizar: {str(e)}', 'danger')
    
    return render_template('autos/editar.html', auto=auto)

@autos_bp.route('/<id>/eliminar', methods=['GET', 'POST'])
def eliminar(id):
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    
    if request.method == 'POST':
        eliminar_auto(current_app.db, id)
        flash('Auto eliminado exitosamente', 'success')
        return redirect(url_for('autos.lista'))
    
    return render_template('autos/eliminar.html', auto=auto)