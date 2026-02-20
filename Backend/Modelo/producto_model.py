from Backend.Modelo.db import get_connection

class ProductoModel:

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        conn.close()
        return productos

    @staticmethod
    def crear(nombre, categoria, precio, stock):
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO productos (nombre, categoria, precio, stock)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, categoria, precio, stock))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(producto_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def actualizar_stock(producto_id, cantidad):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener stock actual
        cursor.execute(
            "SELECT stock FROM productos WHERE id = %s",
            (producto_id,)
        )
        producto = cursor.fetchone()

        if not producto:
            conn.close()
            return False, "Producto no encontrado"

        stock_actual = producto["stock"]
        nuevo_stock = stock_actual + cantidad

        if nuevo_stock < 0:
            conn.close()
            return False, "Stock insuficiente"

        # Actualizar stock
        cursor.execute(
            "UPDATE productos SET stock = %s WHERE id = %s",
            (nuevo_stock, producto_id)
        )

        conn.commit()
        conn.close()
        return True, "Stock actualizado correctamente"

    # ALERTAS DE STOCK BAJO (HU04)
    @staticmethod
    def obtener_stock_bajo(stock_minimo=5):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM productos WHERE stock <= %s",
            (stock_minimo,)
        )
        productos = cursor.fetchall()

        conn.close()
        return productos

    # OBTENER PRODUCTO POR ID (necesario para IA)
    @staticmethod
    def obtener_por_id(producto_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM productos WHERE id = %s",
            (producto_id,)
        )

        producto = cursor.fetchone()

        conn.close()
        return producto
