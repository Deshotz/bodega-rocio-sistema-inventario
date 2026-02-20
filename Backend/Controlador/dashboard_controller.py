from flask import Blueprint, jsonify
from Backend.Modelo.producto_model import ProductoModel
from Backend.Modelo.ventas_model import VentasModel

dashboard_bp = Blueprint("dashboard_bp", __name__)


# =========================
# 📊 KPIs DEL NEGOCIO
# =========================
@dashboard_bp.route("/dashboard/kpis")
def kpis():

    ventas = VentasModel.obtener_todas()
    ventas_totales = len(ventas)

    stock_bajo = len(ProductoModel.obtener_stock_bajo())

    productos = {}

    for v in ventas:
        nombre = v["producto"]
        cantidad = v["cantidad"]

        if nombre not in productos:
            productos[nombre] = 0

        productos[nombre] += cantidad

    producto_top = max(productos, key=productos.get) if productos else "N/A"

    return jsonify({
        "ventas_totales": ventas_totales,
        "stock_bajo": stock_bajo,
        "producto_top": producto_top
    })


# =========================
# 📈 VENTAS POR FECHA
# =========================
@dashboard_bp.route("/dashboard/ventas")
def ventas_por_fecha():

    ventas = VentasModel.obtener_todas()
    resumen = {}

    for v in ventas:
        fecha = str(v["fecha"])[:10]

        if fecha not in resumen:
            resumen[fecha] = 0

        resumen[fecha] += v["cantidad"]

    resultado = [
        {"fecha": f, "total": t}
        for f, t in resumen.items()
    ]

    return jsonify(resultado)
