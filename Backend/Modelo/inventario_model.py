from Backend.Modelo.db import get_connection

class InventarioModel:

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT 
            i.id,
            p.nombre AS producto,
            i.cantidad,
            i.fecha
        FROM inventario i
        JOIN productos p ON i.producto_id = p.id
        ORDER BY i.fecha DESC
        """

        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()
        return datos

    @staticmethod
    def registrar(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO inventario (producto_id, cantidad)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (producto_id, cantidad))
        conn.commit()
        conn.close()
