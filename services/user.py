from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import db, ModeloEvaluacion, AspectoEvaluacion, Pregunta

# Configura el Blueprint con la ruta correcta para las plantillas
admin_blueprint = Blueprint('user', __name__, template_folder='../templates/user/furps_user')




# Ruta para mostrar el modelo FURPS y sus aspectos
@admin_blueprint.route('/furps_user')
def furps_admin():
    # Buscamos el modelo FURPS en la base de datos
    modelo = ModeloEvaluacion.query.filter_by(nombre='FURPS').first()
    if not modelo:
        return "Modelo FURPS no encontrado", 404

    # Obtenemos todos los aspectos relacionados con el modelo FURPS
    aspectos = AspectoEvaluacion.query.filter_by(idmodelo=modelo.idmodelo).all()

    # Renderizamos la plantilla para mostrar los aspectos
    return render_template('furps_user.html', modelo=modelo, aspectos=aspectos)

@admin_blueprint.route('/iso25000_user')
def iso25000_admin():
    # Buscamos el modelo FURPS en la base de datos
    modelo = ModeloEvaluacion.query.filter_by(nombre='ISO25000').first()
    if not modelo:
        return "Modelo ISO25000 no encontrado", 404

    # Obtenemos todos los aspectos relacionados con el modelo FURPS
    aspectos = AspectoEvaluacion.query.filter_by(idmodelo=modelo.idmodelo).all()

    # Renderizamos la plantilla para mostrar los aspectos
    return render_template('iso25000_user.html', modelo=modelo, aspectos=aspectos)



