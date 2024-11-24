from flask import Blueprint, session, redirect, url_for, flash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/seleccionar_modelo/<int:idmodelo>', methods=['GET'])
def seleccionar_modelo(idmodelo):
    # Guardar el ID del modelo seleccionado en la sesión
    session['idmodelo'] = idmodelo
    flash(f'Modelo {idmodelo} seleccionado.', 'success')

    # Redirigir a la lista de aspectos
    return redirect(url_for('aspectos.listar_aspectos'))
