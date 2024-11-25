from flask import Flask, render_template, redirect, url_for, session, flash
from config import Config
from services.models import db, User
from services.auth import auth
from decorators import login_required
from datetime import datetime
from routes import routes
from routes import modulos_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'  # Configuración para guardar sesiones
app.secret_key = 'your_secret_key'  # Clave para proteger las sesiones

db.init_app(app)

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()
    app.register_blueprint(routes, url_prefix="/routes")
    app.register_blueprint(modulos_bp, url_prefix='/modulos')

@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

# Registrar el Blueprint de autenticación
app.register_blueprint(auth, url_prefix="/auth")


# Rutas protegidas para el administrador
@app.route('/dashboard_admin')
@login_required(role='admin')
def dashboard_admin():
    return render_template('dashboard_admin.html')

@app.route('/admin/iso25000_admin')
@login_required(role='admin')
def iso25000_admin():
    return render_template("admin/iso25000_admin.html")

@app.route('/admin/ieee730_admin')
@login_required(role='admin')
def ieee730_admin():
    return render_template("admin/ieee730_admin.html")

@app.route('/admin/furps_admin')
@login_required(role='admin')
def furps_admin():
    return render_template("admin/furps_admin.html")

@app.route('/admin/mccall_admin')
@login_required(role='admin')
def mccall_admin():
    return render_template("admin/mccall_admin.html")

# Rutas protegidas para el usuario
@app.route('/dashboard_user')
@login_required(role='usuario')
def dashboard_user():
    return render_template('dashboard_user.html')

@app.route('/user/dashboard_user_rs')
@login_required(role='usuario')
def dashboard_user_rs():  # Cambiamos el nombre de la función
    return render_template("user/dashboard_user_rs.html")#registro_user

@app.route('/user/iso25000_user')
@login_required(role='usuario')
def iso25000_user():
    return render_template("user/iso25000_user.html")

@app.route('/user/ieee730_user')
@login_required(role='usuario')
def ieee730_user():
    return render_template("user/ieee730_user.html")

@app.route('/user/furps_user')
@login_required(role='usuario')
def furps_user():
    return render_template("user/furps_user.html")

@app.route('/user/mccall_user')
@login_required(role='usuario')
def mccall_user():
    return render_template("user/mccall_user.html")




@app.route('/')
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
