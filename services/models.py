from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
