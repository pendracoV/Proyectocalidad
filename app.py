from flask import Flask, render_template, redirect, url_for, session, flash
from config import Config
from services.models import db
from services.auth import auth

app = Flask(__name__)
app.config.from_object(Config)
app.config['SESSION_TYPE'] = 'filesystem'  # Configuración para guardar sesiones

db.init_app(app)

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

# Registrar el Blueprint de autenticación
app.register_blueprint(auth, url_prefix="/auth")


@app.route('/dashboard_admin')
def dashboard_admin():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        flash("Acceso denegado")
        return redirect(url_for('auth.login'))
    return render_template('dashboard_admin.html')

@app.route('/dashboard_user')
def dashboard_user():
    if 'user_id' not in session or session.get('user_role') != 'usuario':
        flash("Acceso denegado")
        return redirect(url_for('auth.login'))
    return render_template('dashboard_user.html')


@app.route('/admin/iso25000_admin')
def iso25000_admin():
    return render_template("admin/iso25000_admin.html") 

@app.route('/admin/ieee730_admin')
def ieee730_admin():
    return render_template ( "admin/ieee730_admin.html")

@app.route('/admin/furps_admin')
def furps_admin():
    return render_template ("admin/furps_admin.html")

@app.route('/admin/mccall_admin')
def mccall_admin():
    return render_template ("admin/mccall_admin.html")

@app.route('/user/iso25000_user')
def iso25000_user():
    return render_template ("user/iso25000_user.html")

@app.route('/user/ieee730_user')
def ieee730_user():
    return render_template ("user/ieee730_user.html")

@app.route('/user/furps_user')
def furps_user():
    return render_template ("user/furps_user.html")

@app.route('/user/mccall_user')
def mccall_user():
    return render_template ("user/mccall_user.html")

@app.route('/')
def index():
    return render_template ('login.html')

if __name__ == "__main__":
    app.run(debug=True)
