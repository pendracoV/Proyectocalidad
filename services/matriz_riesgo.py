from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import db, MatrizRiesgo, Evaluacion
from flask_login import current_user

# Crear el Blueprint para la matriz de riesgo
matriz_riesgo_bp = Blueprint('matriz_riesgo', __name__)

@matriz_riesgo_bp.route('/', methods=['GET', 'POST'])
def matriz_riesgo():
    if request.method == 'POST':
        # Capturamos los datos del formulario
        descripcion_riesgo = request.form.get('descripcion_riesgo')
        fase_afectada = request.form.get('fase_afectada')
        causa_raiz = request.form.get('causa_raiz')
        entregables_afectados = request.form.get('entregables_afectados')
        objetivo_afectado = request.form.get('objetivo_afectado')
        
        if not all([descripcion_riesgo, fase_afectada, causa_raiz, 
                   entregables_afectados, objetivo_afectado]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(url_for('matriz_riesgo.matriz_riesgo'))
        
        try:
            estimacion_probabilidad = int(request.form.get('estimacion_probabilidad', 0))
            estimacion_impacto = int(request.form.get('estimacion_impacto', 0))
        except (ValueError, TypeError):
            flash('Los valores de probabilidad e impacto deben ser números', 'error')
            return redirect(url_for('matriz_riesgo'))

        nivel_riesgo = calcular_nivel_riesgo(estimacion_probabilidad, estimacion_impacto)
        
        # Crear el objeto con los nombres de columna correctos
        nuevo_riesgo = MatrizRiesgo(
            descripcionriesgo=descripcion_riesgo,
            faseafectada=fase_afectada,
            causaraiz=causa_raiz,
            entregablesafectados=entregables_afectados,
            objetivoafectado=objetivo_afectado,
            estimacionprobabilidad=estimacion_probabilidad,
            estimacionimpacto=estimacion_impacto,
            nivelriesgo=nivel_riesgo,
            idevaluacion=1
        )
        
        db.session.add(nuevo_riesgo)
        db.session.commit()
        return redirect(url_for('matriz_riesgo.matriz_riesgo'))

    # Obtener la matriz de riesgo (si ya existe alguna evaluación)
    matriz = MatrizRiesgo.query.all()  # Se pueden agregar filtros para obtener solo riesgos de la evaluación actual

    return render_template('user/matriz_riesgo.html', matriz=matriz)

def calcular_nivel_riesgo(probabilidad, impacto):
    """
    Calcular el nivel de riesgo basado en la probabilidad y el impacto.
    """
    riesgo = probabilidad * impacto
    if riesgo >= 16:
        return 'Alto'
    elif riesgo >= 9:
        return 'Medio'
    else:
        return 'Bajo'
    