from flask import Blueprint, session, redirect, url_for, flash

dashboard_user_bp = Blueprint('dashboard_user', __name__)

@dashboard_user_bp.route('/seleccionar_modelo_user/<int:idmodelo>', methods=['GET'])
def seleccionar_modelo_user(idmodelo):
    # Guardar el ID del modelo seleccionado en la sesión
    session['idmodelo'] = idmodelo
    flash(f'Modelo {idmodelo} seleccionado.', 'success')

    # Redirigir a la lista de aspectos
    return redirect(url_for('aspectos_user.listar_aspectos_user'))
