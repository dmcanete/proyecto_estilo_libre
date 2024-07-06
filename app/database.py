import os
import mysql.connector
from flask import Flask, g
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos MySQL
DATABASE_CONFIG = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 3306)  # Puerto predeterminado de MySQL
}

# Función para obtener la conexión a la base de datos
def get_db():
    # Si 'db' no está en el contexto global de Flask 'g'
    if 'db' not in g:
        try:
            # Crear una nueva conexión a la base de datos y guardarla en 'g'
            g.db = mysql.connector.connect(**DATABASE_CONFIG)
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise  # Re-lanzar la excepción para manejarla en un nivel superior
    # Retornar la conexión a la base de datos
    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    # Extraer la conexión a la base de datos de 'g' y eliminarla
    db = g.pop('db', None)
    # Si la conexión existe, cerrarla
    if db is not None:
        db.close()

# Función para inicializar la aplicación con el manejo de la base de datos
def init_app(app):
    # Registrar 'close_db' para que se ejecute al final del contexto de la aplicación
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

# Crear una aplicación Flask
app = Flask(__name__)

# Inicializar la aplicación con el manejo de la base de datos
init_app(app)

# Ejemplo de ruta para probar la conexión a la base de datos
@app.route('/')
def index():
    # Obtener una conexión a la base de datos
    db = get_db()
    # Ejemplo de consulta
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tabla_ejemplo")
    result = cursor.fetchall()
    cursor.close()
    # Retornar resultado
    return str(result)

if __name__ == '__main__':
    app.run(debug=True)
