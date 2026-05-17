from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.auto_model import obtener_todos_autos, obtener_auto_por_id

autos_bp = Blueprint('autos', __name__, url_prefix='/autos')

@autos_bp.route('/')
def lista():
    """Página de listado de autos"""
    autos = obtener_todos_autos(current_app.db)
    return render_template('autos/lista.html', autos=autos)

@autos_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    """Página para crear nuevo auto"""
    if request.method == 'POST':
        # TODO: Implementar guardado (Historia HU-01)
        flash('Funcionalidad en construcción', 'info')
        return redirect(url_for('autos.lista'))
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