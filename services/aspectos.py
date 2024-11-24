from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.models import db, AspectoEvaluacion, Pregunta, ModeloEvaluacion

aspectos_bp = Blueprint('aspectos', __name__, template_folder='../templates/aspectos')



@aspectos_bp.route('/aspectos', methods=['GET'])
def listar_aspectos():
    idmodelo = session.get('idmodelo')
    if not idmodelo:
        flash('No se ha seleccionado un modelo.', 'error')
        return redirect(url_for('dashboard'))

    modelo = ModeloEvaluacion.query.get_or_404(idmodelo)
    aspectos = AspectoEvaluacion.query.filter_by(idmodelo=idmodelo).all()

    return render_template('/admin/listar_aspectos.html', modelo=modelo, aspectos=aspectos)


@aspectos_bp.route('/aspectos/agregar', methods=['GET', 'POST'])
def agregar_aspecto():
    idmodelo = session.get('idmodelo')
    if not idmodelo:
        flash('No se ha seleccionado un modelo.', 'error')
        return redirect(url_for('dashboard'))

    modelo = ModeloEvaluacion.query.get_or_404(idmodelo)

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        if nombre and descripcion:
            nuevo_aspecto = AspectoEvaluacion(
                nombre=nombre,
                descripcion=descripcion,
                idmodelo=idmodelo
            )
            db.session.add(nuevo_aspecto)
            db.session.commit()
            flash('Aspecto agregado exitosamente.', 'success')
            return redirect(url_for('aspectos.listar_aspectos'))

        flash('Todos los campos son obligatorios.', 'error')

    return render_template('/admin/agregar_aspecto.html', modelo=modelo)


@aspectos_bp.route('/aspectos/<int:idaspecto>/editar', methods=['GET', 'POST'])
def editar_aspecto(idaspecto):
    idmodelo = session.get('idmodelo')
    if not idmodelo:
        flash('No se ha seleccionado un modelo.', 'error')
        return redirect(url_for('dashboard'))

    modelo = ModeloEvaluacion.query.get_or_404(idmodelo)
    aspecto = AspectoEvaluacion.query.get_or_404(idaspecto)

    if request.method == 'POST':
        aspecto.nombre = request.form.get('nombre')
        aspecto.descripcion = request.form.get('descripcion')

        if aspecto.nombre and aspecto.descripcion:
            db.session.commit()
            flash('Aspecto actualizado exitosamente.', 'success')
            return redirect(url_for('aspectos.listar_aspectos'))

        flash('Todos los campos son obligatorios.', 'error')

    return render_template('/admin/editar_aspecto.html', modelo=modelo, aspecto=aspecto)


@aspectos_bp.route('/aspectos/<int:idaspecto>/eliminar', methods=['POST'])
def eliminar_aspecto(idaspecto):
    idmodelo = session.get('idmodelo')
    if not idmodelo:
        flash('No se ha seleccionado un modelo.', 'error')
        return redirect(url_for('dashboard'))

    aspecto = AspectoEvaluacion.query.get_or_404(idaspecto)
    db.session.delete(aspecto)
    db.session.commit()
    flash('Aspecto eliminado exitosamente.', 'success')
    return redirect(url_for('aspectos.listar_aspectos'))


# Ruta para listar preguntas
@aspectos_bp.route('/<int:idaspecto>/preguntas', methods=['GET'])
def listar_preguntas(idaspecto):
    aspecto = AspectoEvaluacion.query.get_or_404(idaspecto)
    preguntas = Pregunta.query.filter_by(idaspecto=idaspecto).all()
    return render_template('/admin/preguntas.html', aspecto=aspecto, preguntas=preguntas)

# Ruta para agregar una nueva pregunta
@aspectos_bp.route('/<int:idaspecto>/agregar', methods=['GET', 'POST'])
def agregar_pregunta(idaspecto):
    aspecto = AspectoEvaluacion.query.get_or_404(idaspecto)

    if request.method == 'POST':
        textopregunta = request.form.get('textopregunta')
        print(f"Texto recibido: {textopregunta}")  # Depuración
        if textopregunta:
            try:
                nueva_pregunta = Pregunta(textopregunta=textopregunta, idaspecto=idaspecto)
                db.session.add(nueva_pregunta)
                db.session.commit()
                print(f"Pregunta guardada: {nueva_pregunta}")  # Depuración
                flash('Pregunta agregada exitosamente', 'success')
                return redirect(url_for('aspectos.listar_preguntas', idaspecto=idaspecto))
            except Exception as e:
                print(f"Error al guardar en la base de datos: {e}")  # Depuración
                db.session.rollback()  # Revertir cambios si ocurre un error
                flash('Error al agregar la pregunta. Intenta nuevamente.', 'error')
        else:
            flash('El texto de la pregunta no puede estar vacío', 'error')

    return render_template('/admin/agregar_preguntas.html', aspecto=aspecto)


@aspectos_bp.route('/preguntas/<int:idpregunta>/editar', methods=['GET', 'POST'])
def editar_pregunta(idpregunta):
    pregunta = Pregunta.query.get_or_404(idpregunta)

    if request.method == 'POST':
        nuevo_texto = request.form.get('textopregunta')
        if nuevo_texto:
            pregunta.textopregunta = nuevo_texto
            db.session.commit()
            flash('Pregunta editada exitosamente', 'success')
            return redirect(url_for('aspectos.listar_preguntas', idaspecto=pregunta.idaspecto))
        else:
            flash('El texto de la pregunta no puede estar vacío', 'error')

    return render_template('/admin/editar_pregunta.html', pregunta=pregunta)

@aspectos_bp.route('/preguntas/<int:idpregunta>/eliminar', methods=['POST'])
def eliminar_pregunta(idpregunta):
    pregunta = Pregunta.query.get_or_404(idpregunta)
    idaspecto = pregunta.idaspecto  # Para redirigir después de eliminar
    db.session.delete(pregunta)
    db.session.commit()
    flash('Pregunta eliminada exitosamente', 'success')
    return redirect(url_for('aspectos.listar_preguntas', idaspecto=idaspecto))


