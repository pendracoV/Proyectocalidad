import os
#MI COMENTARIO
class Config:
    # Clave secreta de Flask para sesiones y seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # URI de conexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:115689@localhost/saya_tv"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
