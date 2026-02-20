from flask import Blueprint, jsonify, request
from Backend.IA.predecir import predecir_proximos_dias
from Backend.Modelo.producto_model import ProductoModel

ia_bp = Blueprint("ia_bp", __name__)


# =========================================================
# 🔮 1) PREDICCIÓN POR PRODUCTO
# =========================================================
@ia_bp.route("/ia/prediccion/<int:producto_id>", methods=["GET"])
def prediccion(producto_id):

    try:
        dias = request.args.get("dias", default=7, type=int)

        if dias <= 0 or dias > 30:
            return jsonify({"error": "Número de días inválido"}), 400

        resultado = predecir_proximos_dias(producto_id, dias)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 📦 2) REABASTECIMIENTO POR PRODUCTO
# =========================================================
@ia_bp.route("/ia/reabastecimiento/<int:producto_id>", methods=["GET"])
def reabastecimiento(producto_id):

    try:
        dias = request.args.get("dias", default=7, type=int)

        if dias <= 0 or dias > 30:
            return jsonify({"error": "Número de días inválido"}), 400

        predicciones = predecir_proximos_dias(producto_id, dias)
        demanda_total = sum(p["demanda_predicha"] for p in predicciones)

        producto = ProductoModel.obtener_por_id(producto_id)

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        stock_actual = producto["stock"]

        recomendacion = max(0, int(demanda_total - stock_actual))

        return jsonify({
            "demanda_estimada": round(demanda_total, 2),
            "stock_actual": stock_actual,
            "recomendacion_compra": recomendacion
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================================================
# 🌍 3) RECOMENDACIÓN GLOBAL (TODOS LOS PRODUCTOS)
# =========================================================
@ia_bp.route("/ia/recomendacion-global", methods=["GET"])
def recomendacion_global():

    try:
        dias = request.args.get("dias", default=7, type=int)

        productos = ProductoModel.obtener_todos()

        compra_total = 0

        for p in productos:

            predicciones = predecir_proximos_dias(p["id"], dias)

            demanda = sum(d["demanda_predicha"] for d in predicciones)

            stock = p["stock"]

            compra = max(0, int(demanda - stock))

            compra_total += compra

        return jsonify({
            "recomendacion_compra": compra_total
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
