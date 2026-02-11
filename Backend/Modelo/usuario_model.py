from Backend.Modelo.db import get_connection

class UsuarioModel:

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, nombre, correo, rol FROM usuarios")
        usuarios = cursor.fetchall()

        conn.close()
        return usuarios

    @staticmethod
    def crear(nombre, correo, password, rol="usuario"):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO usuarios (nombre, correo, password, rol)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, correo, password, rol))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(usuario_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
        conn.commit()
        conn.close()

    # ✅ NUEVO – LOGIN (HU05)
    @staticmethod
    def login(correo, password):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE correo = %s AND password = %s
        """

        cursor.execute(sql, (correo, password))
        usuario = cursor.fetchone()

        conn.close()
        return usuario
