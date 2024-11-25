from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from services.models import db, Evaluacion
from datetime import datetime
from sqlalchemy import text

routes = Blueprint('routes', __name__)

@routes.route('/submit_evaluation', methods=['POST'])
def submit_evaluation():
    nombresoftware = request.form['nombresoftware']
    empresa = request.form['empresa']
    ciudad = request.form['ciudad']
    telefono = request.form['telefono']
    fechaevaluacion = request.form['fechaevaluacion']
    idmodelo = request.form.get('idmodelo')  # Capturar el ID del modelo
    idusuario = session.get('user_id')  # Obtener el ID del usuario de la sesión

    if not idusuario:
        flash('Debes iniciar sesión para enviar una evaluación.', 'danger')
        return redirect(url_for('auth.login'))

    if not idmodelo:
        flash('Debes seleccionar un modelo.', 'danger')
        return redirect(url_for('routes.dashboard_user'))

    try:
        nueva_evaluacion = Evaluacion(
            idusuario=idusuario,
            nombresoftware=nombresoftware,
            empresa=empresa,
            ciudad=ciudad,
            telefono=telefono,
            fechaevaluacion=datetime.strptime(fechaevaluacion, '%Y-%m-%d'),
            idmodelo=int(idmodelo)  # Asegurarse de convertirlo a entero
        )

        db.session.add(nueva_evaluacion)
        db.session.commit()

        flash('Evaluación enviada exitosamente.', 'success')
        return redirect(url_for('routes.dashboard_user'))
    except Exception as e:
        current_app.logger.error(f"Error al guardar la evaluación: {e}")
        flash(f'Error al guardar la evaluación: {e}', 'danger')
        return redirect(url_for('routes.dashboard_user'))
    
@routes.route('/dashboard_user')
def dashboard_user():
    return render_template('dashboard_user.html')

#  Para obtener los modelos en el SELECT
# Crear el Blueprint
modulos_bp = Blueprint('modulos', __name__)

# Función para obtener los modelos desde la base de datos
@modulos_bp.route('/get-modelos', methods=['GET'])
def get_modelos():
    try:
        # Declarar la consulta explícitamente como texto
        query = text("SELECT idmodelo, nombre FROM public.modeloevaluacion ORDER BY idmodelo ASC;")
        result = db.session.execute(query)

        # Convertir los resultados a JSON
        modelos = [{"idmodelo": row[0], "nombre": row[1]} for row in result.fetchall()]

        return jsonify(modelos)
    except Exception as e:
        current_app.logger.error(f"Error al obtener los modelos: {e}")
        return jsonify({"error": str(e)}), 500