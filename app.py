from flask import Flask, render_template, request
import pymysql as sql

app = Flask(__name__)

# Conexión a MySQL
class Database:
    def __init__(self, host=None, user=None, password=None, database=None, port=None):
        self.host = host or '192.168.252.35'
        self.user = user or 'D_PERSONAL'
        self.password = password or 'ScadaEMEMSA40'
        self.database = database or 'info_scada'
        self.port = port or 3306
        self.connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )

    def crear_tabla_si_no_existe(self):
        self.connect()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS encuesta (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100),
                    respuesta VARCHAR(20)
                )
            """)
        self.connection.commit()

    def guardar_respuesta(self, nombre, respuesta):
        self.connect()
        self.crear_tabla_si_no_existe()
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO encuesta (nombre, repuesta) VALUES (%s, %s)", (nombre, respuesta))
        self.connection.commit()

db = Database()

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form.get('nombre')
    mensaje = request.form.get('mensaje')
    
    # Puedes hacer lo que quieras con los datos: imprimir, guardar, etc.
    db.guardar_respuesta(nombre, mensaje)
    print(f'Nombre: {nombre}')
    print(f'Mensaje: {mensaje}')
    
    return f"<h2>Formulario recibido</h2><p>Nombre: {nombre}</p><p>Mensaje: {mensaje}</p>"

if __name__ == "__main__":
    app.run(debug=True)
