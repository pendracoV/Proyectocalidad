from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from services.models import db, Evaluacion

registrar_software_bp = Blueprint('registrar_software', __name__)

@registrar_software_bp.route('/registrar', methods=['GET', 'POST'])
def registrar_software():
    # Obtener el ID del modelo desde la sesión
    idmodelo = session.get('idmodelo')  # Correctamente accediendo a session

    if not idmodelo:
        flash('Por favor, selecciona un modelo antes de registrar el software.', 'error')
        return redirect(url_for('dashboard_user.dashboard'))

    if request.method == 'GET':
        # Renderizar la plantilla para registrar software
        return render_template('/user/registrar_software.html', idmodelo=idmodelo)

    # Si es una solicitud POST
    nombresoftware = request.form.get('nombresoftware')
    empresa = request.form.get('empresa')
    ciudad = request.form.get('ciudad')
    telefono = request.form.get('telefono')
    fechaevaluacion = request.form.get('fechaevaluacion') or datetime.now().strftime('%Y-%m-%d')

    # Validar campos obligatorios
    if not (nombresoftware and empresa and ciudad and telefono):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('registrar_software.registrar_software'))

    # Obtener el ID del usuario desde la sesión
    idusuario = session.get('user_id')
    if not idusuario:
        flash('Usuario no autenticado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('auth.login'))

    # Crear una nueva evaluación incluyendo el idmodelo
    nueva_evaluacion = Evaluacion(
        idusuario=idusuario,
        idmodelo=idmodelo,  # Este es el valor del modelo
        nombresoftware=nombresoftware,
        empresa=empresa,
        ciudad=ciudad,
        telefono=telefono,
        fechaevaluacion=fechaevaluacion
    )

    try:
        # Guardar en la base de datos
        db.session.add(nueva_evaluacion)
        db.session.commit()
        flash('Software registrado exitosamente.', 'success')
        
        # Obtener el nombre del software registrado
        nombresoftware = nueva_evaluacion.nombresoftware
        
        # Renderizar la plantilla de aspecto, pasando el nombre del software
        return redirect(url_for('aspectos_user.listar_aspectos_user', nombresoftware=nombresoftware))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al registrar el software: {e}', 'error')
        return redirect(url_for('registrar_software.registrar_software'))

##################################################
from flask import Blueprint, request, jsonify
from services.models import db, Evaluacion

@registrar_software_bp.route('/actualizar_resultadoglobal', methods=['POST'])
def actualizar_resultadoglobal():
    data = request.get_json()
    idevaluacion = data.get('idevaluacion')
    resultadoglobal = data.get('resultadoglobal')

    if not idevaluacion or resultadoglobal is None:
        return jsonify({'success': False, 'message': 'Datos incompletos.'}), 400

    try:
        # Buscar la evaluación correspondiente
        evaluacion = Evaluacion.query.get(idevaluacion)
        if not evaluacion:
            return jsonify({'success': False, 'message': 'Evaluación no encontrada.'}), 404

        # Actualizar el resultado global
        evaluacion.resultadoglobal = resultadoglobal
        db.session.commit()

        return jsonify({'success': True, 'message': 'Resultado global actualizado correctamente.'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al actualizar: {str(e)}'}), 500
