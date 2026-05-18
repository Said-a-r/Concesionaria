from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.auto_model import crear_auto, obtener_todos_autos, obtener_auto_por_id, actualizar_auto, eliminar_auto
import os
from werkzeug.utils import secure_filename
from datetime import datetime

import os
from werkzeug.utils import secure_filename
from datetime import datetime


autos_bp = Blueprint('autos', __name__, url_prefix='/autos')

# ========== FUNCIONES AUXILIARES ==========

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
        
        # Crear carpeta si no existe
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        archivo.save(ruta_guardado)
        return f"/static/uploads/{nombre_unico}"
    return None

# ========== RUTAS CRUD ==========

@autos_bp.route('/')
def lista():
    """Página de listado de autos"""
    autos = obtener_todos_autos(current_app.db)
    return render_template('autos/lista.html', autos=autos)

@autos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        try:
            # 1. Obtener datos del formulario
            datos = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'),
                'año': int(request.form.get('año')),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria': request.form.get('categoria'),
                'imagen_url': current_app.config['DEFAULT_IMAGE']
            }
            
            # 2. Validaciones básicas
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
            
            # 3. Manejar imagen (si viene del formulario)
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
    """Página de detalle de un auto"""
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    return render_template('autos/detalle.html', auto=auto)

@autos_bp.route('/<id>/editar', methods=['GET', 'POST'])
def editar(id):
    """Página para editar un auto"""
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
            
            # Mantener imagen actual o actualizar si se sube nueva
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
    """Página para eliminar un auto con confirmación"""
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    
    if request.method == 'POST':
        eliminar_auto(current_app.db, id)
        flash('Auto eliminado exitosamente', 'success')
        return redirect(url_for('autos.lista'))
    
    return render_template('autos/eliminar.html', auto=auto)