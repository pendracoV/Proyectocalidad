from flask import (
    Blueprint, render_template, request, redirect, url_for, 
    session, flash, current_app, jsonify
)
from services.models import db, Evaluacion
from datetime import datetime
from sqlalchemy import text

# Crear el Blueprint para las rutas
routes = Blueprint('routes', __name__)

@routes.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    """
    Procesa la evaluación enviada por el usuario.
    """
    # Obtener datos del formulario
    nombresoftware = request.form.get('nombresoftware')
    empresa = request.form.get('empresa')
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')
    fechaevaluacion = request.form.get('fechaevaluacion')
    idusuario = session.get('user_id')  # Obtener el ID del usuario de la sesión

    # Validaciones iniciales
    if not idusuario:
        flash('Debes iniciar sesión para enviar una evaluación.', 'danger')
        return redirect(url_for('auth.login'))

    
    from services.models import get_questions_by_model

    
    try:
        # Crear la nueva evaluación
        nueva_evaluacion = Evaluacion(
            idusuario=idusuario,
            nombresoftware=nombresoftware,
            empresa=empresa,
            ciudad=ciudad,
            telefono=telefono,
            fechaevaluacion=datetime.strptime(fechaevaluacion, '%Y-%m-%d'), # Convertir a entero si es necesario
        )

        # Guardar en la base de datos
        db.session.add(nueva_evaluacion)
        db.session.commit()

          # Redirigir con parámetro de éxito
        return redirect(url_for('routes.dashboard_user', success='true'))
    except Exception as e:
        current_app.logger.error(f"Error al guardar la evaluación: {e}")
        flash(f'Error al guardar la evaluación: {e}', 'danger')
        return redirect(url_for('routes.dashboard_user'))



# Crear otro Blueprint para manejar modelos
modulos_bp = Blueprint('modulos', __name__)
@routes.route('/dashboard_user')
def dashboard_user():
    return render_template('dashboard_user.html')
  
