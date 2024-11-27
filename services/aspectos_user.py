from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.models import db, AspectoEvaluacion, Pregunta, ModeloEvaluacion

aspectos_user_bp = Blueprint('aspectos_user', __name__, template_folder='../templates/aspectos_user')



@aspectos_user_bp.route('/aspectos_user', methods=['GET'])
def listar_aspectos_user():
    idmodelo = session.get('idmodelo')
    if not idmodelo:
        flash('No se ha seleccionado un modelo.', 'error')
        return redirect(url_for('dashboard_user'))

    modelo = ModeloEvaluacion.query.get_or_404(idmodelo)
    aspectos = AspectoEvaluacion.query.filter_by(idmodelo=idmodelo).all()

    return render_template('/user/listar_aspectos_user.html', modelo=modelo, aspectos=aspectos)

# Ruta para listar preguntas
@aspectos_user_bp.route('/<int:idaspecto>/preguntas', methods=['GET'])
def listar_preguntas_user(idaspecto):
    aspecto = AspectoEvaluacion.query.get_or_404(idaspecto)
    preguntas = Pregunta.query.filter_by(idaspecto=idaspecto).all()
    return render_template('/user/preguntas_user.html', aspecto=aspecto, preguntas=preguntas)

