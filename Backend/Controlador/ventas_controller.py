from flask import Blueprint, request, jsonify
from Backend.Modelo.ventas_model import VentasModel
from Backend.Modelo.producto_model import ProductoModel

ventas_bp = Blueprint("ventas_bp", __name__)

# Registrar venta
@ventas_bp.route("/ventas", methods=["POST"])
def registrar_venta():
    data = request.json

    try:
        producto_id = int(data["producto_id"])
        cantidad = int(data["cantidad"])
    except:
        return jsonify({"error": "Datos inválidos"}), 400

    # Registrar venta
    VentasModel.registrar(producto_id, cantidad)

    # Descontar stock
    exito, mensaje = ProductoModel.actualizar_stock(producto_id, -cantidad)

    if not exito:
        return jsonify({"error": mensaje}), 400

    return jsonify({"mensaje": "Venta registrada correctamente"})


# Listar ventas
@ventas_bp.route("/ventas", methods=["GET"])
def listar_ventas():
    ventas = VentasModel.obtener_todas()
    return jsonify(ventas)
