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


@app.route('/')
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
