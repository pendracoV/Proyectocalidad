from flask import redirect, url_for, session, flash
from functools import wraps

def login_required(role=None):
    """
    Decorador para proteger rutas según el rol del usuario.
    Si 'role' es 'admin', solo los administradores pueden acceder.
    Si 'role' es 'usuario', solo los usuarios normales pueden acceder.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash("Por favor, inicia sesión primero.")
                return redirect(url_for('auth.login'))
            
            # Verificar el rol del usuario
            if role and session.get('user_role') != role:
                flash("Acceso denegado.")
                return redirect(url_for('auth.login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
