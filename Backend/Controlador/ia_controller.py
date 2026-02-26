from flask import Blueprint, jsonify, request
from Backend.IA.predecir import predecir_proximos_dias
from Backend.Modelo.producto_model import ProductoModel

ia_bp = Blueprint("ia_bp", __name__)

# 🔮 PREDICCIÓN
@ia_bp.route("/ia/prediccion/<int:producto_id>", methods=["GET"])
def prediccion(producto_id):
    try:
        dias = request.args.get("dias", default=7, type=int)

        if dias <= 0 or dias > 30:
            return jsonify({"error": "Número de días inválido"}), 400

        producto = ProductoModel.obtener_por_id(producto_id)

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        resultado = predecir_proximos_dias(producto_id, dias)

        return jsonify({
            "producto": producto["nombre"],
            "tipo_producto": producto["tipo_producto"],
            "clasificacion_abc": producto["clasificacion_abc"],
            "nivel_criticidad": producto["nivel_criticidad"],
            "lead_time": producto["lead_time"],
            "predicciones": resultado
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📦 REABASTECIMIENTO INTELIGENTE (usa lead_time real)
@ia_bp.route("/ia/reabastecimiento/<int:producto_id>", methods=["GET"])
def reabastecimiento(producto_id):

    try:
        producto = ProductoModel.obtener_por_id(producto_id)

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        # 🔥 usar lead_time real
        dias = producto["lead_time"]

        predicciones = predecir_proximos_dias(producto_id, dias)
        demanda_total = sum(p["demanda_predicha"] for p in predicciones)

        stock_actual = producto["stock"]

        recomendacion = max(0, int(demanda_total - stock_actual))

        return jsonify({
            "demanda_estimada": round(demanda_total, 2),
            "stock_actual": stock_actual,
            "recomendacion_compra": recomendacion,
            "nivel_criticidad": producto["nivel_criticidad"],
            "lead_time": producto["lead_time"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500