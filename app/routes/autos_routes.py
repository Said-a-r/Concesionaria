from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.auto_model import obtener_todos_autos, obtener_auto_por_id

import os
from werkzeug.utils import secure_filename
from datetime import datetime


autos_bp = Blueprint('autos', __name__, url_prefix='/autos')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def guardar_imagen(archivo):
    if archivo and archivo.filename != '' and allowed_file(archivo.filename):

        nombre_seguro = secure_filename(archivo.filename)

        nombre_unico = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nombre_seguro}"

        ruta_guardado = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            nombre_unico
        )

        archivo.save(ruta_guardado)

        return f"/static/uploads/{nombre_unico}"

    return "/static/uploads/default.jpg"


@autos_bp.route('/')
def lista():
    """Página de listado de autos"""
    autos = obtener_todos_autos(current_app.db)
    return render_template('autos/lista.html', autos=autos)

@autos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':

        try:

            datos = {
                'marca': request.form.get('marca'),
                'modelo': request.form.get('modelo'),
                'año': int(request.form.get('año')),
                'precio': float(request.form.get('precio')),
                'stock': int(request.form.get('stock')),
                'categoria': request.form.get('categoria'),
                'imagen_url': '/static/uploads/default.jpg'
            }

            # Manejar imagen
            if 'imagen' in request.files:

                archivo = request.files['imagen']

                datos['imagen_url'] = guardar_imagen(archivo)

            flash('Imagen procesada correctamente', 'success')

            return redirect(url_for('autos.lista'))

        except Exception as e:

            flash(f'Error: {str(e)}', 'danger')

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
        # TODO: Implementar edición
        flash('Funcionalidad en construcción', 'info')
        return redirect(url_for('autos.lista'))
    
    return render_template('autos/editar.html', auto=auto)

@autos_bp.route('/<id>/eliminar', methods=['GET', 'POST'])
def eliminar(id):
    """Página para eliminar un auto con confirmación"""
    auto = obtener_auto_por_id(current_app.db, id)
    if not auto:
        flash('Auto no encontrado', 'danger')
        return redirect(url_for('autos.lista'))
    
    if request.method == 'POST':
        # TODO: Implementar eliminación
        flash('Funcionalidad en construcción', 'info')
        return redirect(url_for('autos.lista'))
    
    return render_template('autos/eliminar.html', auto=auto)