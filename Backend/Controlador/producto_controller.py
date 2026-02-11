from flask import Blueprint, request, jsonify
from Backend.Modelo.producto_model import ProductoModel
from Backend.Modelo.inventario_model import InventarioModel

producto_bp = Blueprint("producto_bp", __name__)

# 🔹 Listar productos
@producto_bp.route("/productos", methods=["GET"])
def listar_productos():
    productos = ProductoModel.obtener_todos()
    return jsonify(productos)

# 🔹 Crear producto
@producto_bp.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json

    ProductoModel.crear(
        data["nombre"],
        data["categoria"],
        data["precio"],
        data["stock"]
    )

    return jsonify({"mensaje": "Producto creado correctamente"})

# 🔹 Eliminar producto
@producto_bp.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    ProductoModel.eliminar(id)
    return jsonify({"mensaje": "Producto eliminado correctamente"})

# 🔹 Actualizar stock (+ o -)
@producto_bp.route("/productos/<int:id>/stock", methods=["PUT"])
def actualizar_stock(id):
    data = request.json
    cantidad = data.get("cantidad")

    if cantidad is None:
        return jsonify({"error": "Cantidad requerida"}), 400

    exito, mensaje = ProductoModel.actualizar_stock(id, cantidad)

    if not exito:
        return jsonify({"error": mensaje}), 400

    # Registrar movimiento en inventario
    InventarioModel.registrar(id, cantidad)

    return jsonify({"mensaje": mensaje})

# 🔴 ALERTAS DE STOCK BAJO
@producto_bp.route("/productos/stock-bajo", methods=["GET"])
def productos_stock_bajo():
    productos = ProductoModel.obtener_stock_bajo()
    return jsonify(productos)
