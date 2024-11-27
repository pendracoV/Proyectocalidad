from flask import Flask, render_template, redirect, url_for, session, flash
from config import Config
from services.models import db, User
from services.auth import auth
from services.aspectos import aspectos_bp
from services.aspectos_user import aspectos_user_bp # Importa el Blueprint
from decorators import login_required
from services.dashboard import dashboard_bp
from services.dashboard_user import dashboard_user_bp
from services.registrar_software import registrar_software_bp
from datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'  # Configuración para guardar sesiones
app.secret_key = 'your_secret_key'  # Clave para proteger las sesiones

db.init_app(app)

# Crear las tablas en la base de datos si no existen

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

app.register_blueprint(registrar_software_bp, url_prefix='/software')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(aspectos_bp, url_prefix="/aspectos") 
app.register_blueprint(dashboard_user_bp, url_prefix='/dashboard_user')
app.register_blueprint(aspectos_user_bp, url_prefix="/aspectos_user") 
app.register_blueprint(auth, url_prefix="/auth")
#####################################


# Rutas protegidas para el administrador
@app.route('/dashboard_admin')
@login_required(role='admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')


# Rutas protegidas para el usuario
@app.route('/dashboard_user')
@login_required(role='usuario')
def dashboard_user():
    return render_template('dashboard_user.html') 







@app.route('/')
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
