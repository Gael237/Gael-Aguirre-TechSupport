from flask import Flask, request, jsonify
import pymysql
import os
import requests

app = Flask(__name__)

# conexión a base de datos
def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )

# ------------------ HTML PRINCIPAL ------------------
@app.route("/", methods=["GET"])
def home():
    return """
    <h1>Soporte Técnico</h1>

    <h2>Crear Ticket</h2>
    <form action="/crear_ticket" method="post">
        Nombre: <input name="nombre"><br>
        Email: <input name="email"><br>
        Titulo: <input name="titulo"><br>
        Descripcion: <input name="descripcion"><br>

        Prioridad:
        <select name="prioridad">
            <option value="baja">Baja</option>
            <option value="media">Media</option>
            <option value="alta">Alta</option>
        </select><br><br>

        <button type="submit">Crear Ticket</button>
    </form>

    <br><a href="/tickets">Ver Tickets</a>
    """

# ------------------ CREAR TICKET ------------------
@app.route("/crear_ticket", methods=["POST"])
def crear_ticket():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        nombre = request.form["nombre"]
        email = request.form["email"]
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        prioridad = request.form["prioridad"]

        # insertar cliente
        cursor.execute(
            "INSERT INTO clientes (nombre, email) VALUES (%s, %s)",
            (nombre, email)
        )
        cliente_id = cursor.lastrowid

        # insertar ticket
        cursor.execute(
            """INSERT INTO tickets (cliente_id, titulo, descripcion, prioridad)
               VALUES (%s, %s, %s, %s)""",
            (cliente_id, titulo, descripcion, prioridad)
        )

        conn.commit()

        # -------- LLAMADA A SERVICIO B --------
        try:
            requests.post("http://servicio_b:5001/procesar")
        except Exception as e:
            print("Servicio B no disponible:", e)

        return "<h3>Ticket creado correctamente</h3><a href='/'>Volver</a>"

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ------------------ CONSULTAR TICKETS ------------------
@app.route("/tickets", methods=["GET"])
def ver_tickets():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.id, c.nombre, t.titulo, t.prioridad, t.estado
            FROM tickets t
            JOIN clientes c ON t.cliente_id = c.id
            ORDER BY FIELD(t.prioridad, 'alta', 'media', 'baja')
        """)

        data = cursor.fetchall()

        html = "<h1>Tickets</h1><ul>"
        for row in data:
            html += f"<li>ID:{row[0]} | Cliente:{row[1]} | {row[2]} | {row[3]} | {row[4]}</li>"
        html += "</ul><a href='/'>Volver</a>"

        return html

    except Exception as e:
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ------------------ ACTUALIZAR ESTADO ------------------
@app.route("/estado", methods=["POST"])
def actualizar_estado():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        ticket_id = request.form["ticket_id"]
        estado = request.form["estado"]

        cursor.execute(
            "UPDATE tickets SET estado=%s WHERE id=%s",
            (estado, ticket_id)
        )

        conn.commit()

        return "Estado actualizado"

    except Exception as e:
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ------------------ ASIGNAR TECNICO ------------------
@app.route("/asignar", methods=["POST"])
def asignar():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        ticket_id = request.form["ticket_id"]
        tecnico_id = request.form["tecnico_id"]

        cursor.execute(
            "UPDATE tickets SET tecnico_id=%s WHERE id=%s",
            (tecnico_id, ticket_id)
        )

        conn.commit()

        return "Técnico asignado"

    except Exception as e:
        return str(e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
