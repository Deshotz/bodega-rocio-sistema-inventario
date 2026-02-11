from flask import Blueprint, request, jsonify
from Backend.Modelo.inventario_model import InventarioModel

inventario_bp = Blueprint("inventario_bp", __name__)

@inventario_bp.route("/inventario", methods=["GET"])
def listar_inventario():
    return jsonify(InventarioModel.obtener_todos())

@inventario_bp.route("/inventario", methods=["POST"])
def registrar_movimiento():
    data = request.json
    InventarioModel.registrar(
        data["producto_id"],
        data["cantidad"]
    )
    return jsonify({"mensaje": "Movimiento registrado"})
