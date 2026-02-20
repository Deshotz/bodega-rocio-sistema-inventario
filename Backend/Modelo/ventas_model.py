from Backend.Modelo.db import get_connection


class VentasModel:

    @staticmethod
    def registrar(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO ventas (producto_id, cantidad)
        VALUES (%s, %s)
        """
        cursor.execute(sql, (producto_id, cantidad))

        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todas():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT v.id, p.nombre AS producto, v.cantidad, v.fecha
        FROM ventas v
        JOIN productos p ON v.producto_id = p.id
        ORDER BY v.fecha DESC
        """

        cursor.execute(query)
        ventas = cursor.fetchall()

        conn.close()
        return ventas

    # 🔥 PRODUCTO MÁS VENDIDO
    @staticmethod
    def obtener_producto_mas_vendido():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT producto_id, SUM(cantidad) AS total
        FROM ventas
        GROUP BY producto_id
        ORDER BY total DESC
        LIMIT 1
        """

        cursor.execute(query)
        resultado = cursor.fetchone()

        conn.close()

        if resultado:
            return resultado["producto_id"]

        return None
