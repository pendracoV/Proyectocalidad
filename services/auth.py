from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.models import db, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']

        # Verificar que las contraseñas coincidan
        if password != confirmpassword:
            error = "Las contraseñas no coinciden"
            return render_template('register.html', error=error)
        
        # Verificar si el email ya está registrado
        if User.query.filter_by(email=email).first():
            error = "El email ya está registrado"
            return render_template('register.html', error=error)

        # Crear nuevo usuario y guardar en la base de datos
        user = User(nombre=nombre, apellido=apellido, email=email)
        user.set_password(password)  # Guarda la contraseña encriptada
        db.session.add(user)
        db.session.commit()

        # Redirigir al login tras el registro exitoso
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Guarda el ID y el rol del usuario en la sesión
            session['user_id'] = user.id
            session['user_role'] = user.rol
            
            # Redirecciona según el rol del usuario
            if user.rol == 'admin':
                return redirect(url_for('dashboard_admin'))
            elif user.rol == 'usuario':
                return redirect(url_for('dashboard_user'))
            else:
                # Si el rol no es reconocido, redirige a una página por defecto o de error
                flash("Rol no reconocido. Contacte al administrador.")
                return redirect(url_for('auth.login'))
        else:
            # Si el login falla, muestra un mensaje de error
            error = "Email o contraseña incorrectos"
            return render_template('login.html', error=error)

    return render_template('login.html')

@auth.route('/logout')
def logout():
    # Eliminar datos de sesión
    session.pop('user_id', None)
    session.pop('user_role', None)
    flash("Sesión cerrada exitosamente")
    return redirect(url_for('auth.login'))

