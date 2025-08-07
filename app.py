from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Conexión a base de datos
def guardar_en_bd(nombre, respuesta):
    conn = sqlite3.connect("datos.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS encuestas (nombre TEXT, respuesta TEXT)")
    cursor.execute("INSERT INTO encuestas (nombre, respuesta) VALUES (?, ?)", (nombre, respuesta))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        respuesta = request.form["respuesta"]
        guardar_en_bd(nombre, respuesta)
        return "¡Gracias por tu respuesta!"
    return render_template("formulario.html")

if __name__ == "__main__":
    app.run(debug=True)
