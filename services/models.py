from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña_hash = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    rol = db.Column(db.String(50), nullable=False, default="usuario")

    def set_password(self, password):
        """Hash la contraseña y la guarda en el campo `contraseña_hash`."""
        self.contraseña_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verifica la contraseña proporcionada contra el hash guardado."""
        return check_password_hash(self.contraseña_hash, password)

    def __repr__(self):
        return f'<Usuario {self.nombre} {self.apellido}>'
    

class ModeloEvaluacion(db.Model):
    __tablename__ = 'modeloevaluacion'

    idmodelo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    # Relación con AspectoEvaluacion
    aspectos = db.relationship('AspectoEvaluacion', backref='modelo', lazy=True)

    def __repr__(self):
        return f"<ModeloEvaluacion id={self.idmodelo}, nombre={self.nombre}>"

# Modelo de AspectoEvaluacion
class AspectoEvaluacion(db.Model):
    __tablename__ = 'aspectoevaluacion'

    idaspecto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    idmodelo = db.Column(db.Integer, db.ForeignKey('modeloevaluacion.idmodelo'), nullable=False)

    def __repr__(self):
        return f"<AspectoEvaluacion id={self.idaspecto}, nombre={self.nombre}>"

# Modelo de Pregunta
class Pregunta(db.Model):
    __tablename__ = 'pregunta'

    idpregunta = db.Column(db.Integer, primary_key=True)
    textopregunta = db.Column(db.Text, nullable=False)
    idaspecto = db.Column(db.Integer, db.ForeignKey('aspectoevaluacion.idaspecto'), nullable=False)
    aspecto = db.relationship('AspectoEvaluacion', backref='preguntas')

    def __repr__(self):
        return f"<Pregunta id={self.idpregunta}, texto={self.textopregunta[:30]}...>"

# Modelo de Evaluación por Usuario
class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'

    idevaluacion = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    idmodelo = db.Column(db.Integer, db.ForeignKey('modeloevaluacion.idmodelo'), nullable=False)
    fechaevaluacion = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    nombresoftware = db.Column(db.String(100), nullable=False)
    empresa = db.Column(db.String(100), nullable=True)
    ciudad = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    resultadoglobal = db.Column(db.Float, nullable=True)

    # Relación con RespuestaEvaluacion
    respuestas = db.relationship('RespuestaEvaluacion', backref='evaluacion', lazy=True)

    def __repr__(self):
        return f"<Evaluacion id={self.idevaluacion}, software={self.nombresoftware}>"

# Modelo de Respuesta de Evaluación
class RespuestaEvaluacion(db.Model):
    __tablename__ = 'respuestaevaluacion'

    idrespuesta = db.Column(db.Integer, primary_key=True)
    idevaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.idevaluacion'), nullable=False)
    idpregunta = db.Column(db.Integer, db.ForeignKey('pregunta.idpregunta'), nullable=False)
    puntaje = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<RespuestaEvaluacion id={self.idrespuesta}, puntaje={self.puntaje}>"

# services/models.py

#######################################
def get_questions_by_model(idmodelo):
    """
    Obtiene las preguntas asociadas a un modelo de evaluación.
    
    :param idmodelo: ID del modelo de evaluación seleccionado.
    :return: Lista de preguntas asociadas al modelo.
    """
    # Realiza la consulta para obtener las preguntas
    preguntas = (
        db.session.query(Pregunta)
        .join(AspectoEvaluacion, Pregunta.idaspecto == AspectoEvaluacion.idaspecto)
        .filter(AspectoEvaluacion.idmodelo == idmodelo)
        .all()
    )
    return preguntas


class MatrizRiesgo(db.Model):
    __tablename__ = 'matrizriesgo'

    # Definimos las columnas de la tabla
    idmatriz = db.Column(db.Integer, primary_key=True)
    idevaluacion = db.Column(db.Integer, db.ForeignKey('evaluacion.idevaluacion'), nullable=False)
    descripcionriesgo = db.Column(db.Text, nullable=False)
    faseafectada = db.Column(db.String(50), nullable=False)
    causaraiz = db.Column(db.Text, nullable=False)
    entregablesafectados = db.Column(db.Text, nullable=True)
    objetivoafectado = db.Column(db.String(50), nullable=True)
    estimacionprobabilidad = db.Column(db.Integer, nullable=False)
    estimacionimpacto = db.Column(db.Integer, nullable=False)
    nivelriesgo = db.Column(db.String(20), nullable=True)

    # Relación con la tabla Evaluacion
    evaluacion = db.relationship('Evaluacion', backref='matricesriesgo', lazy=True)

    def _repr_(self):
        return f"<MatrizRiesgo id={self.idmatriz}, Evaluacion={self.idevaluacion}>"