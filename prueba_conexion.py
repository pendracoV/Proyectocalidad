import psycopg2
from psycopg2 import OperationalError

def check_db_connection():
    try:
        # Configura los parámetros de conexión
        connection = psycopg2.connect(
            dbname="saya",
            user="postgres",
            password="115689",
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("✅ Conexión exitosa a la base de datos PostgreSQL")
        print(f"Versión de PostgreSQL: {db_version[0]}")
        
        # Cerrar la conexión y el cursor
        cursor.close()
        connection.close()
        
    except OperationalError as e:
        print("❌ Error al conectar con la base de datos")
        print(f"Detalles del error: {e}")

if __name__ == "__main__":
    check_db_connection()
