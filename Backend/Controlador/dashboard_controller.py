from flask import Blueprint, jsonify
from Backend.Modelo.producto_model import ProductoModel
from Backend.Modelo.ventas_model import VentasModel

dashboard_bp = Blueprint("dashboard_bp", __name__)

# =========================
# 📊 KPIs ESTRATÉGICOS
# =========================
@dashboard_bp.route("/dashboard/kpis")
def kpis():

    ventas = VentasModel.obtener_todas()
    productos = ProductoModel.obtener_todos()

    ventas_totales = len(ventas)

    # 🔥 Producto más vendido
    conteo = {}
    for v in ventas:
        nombre = v["producto"]
        cantidad = v["cantidad"]
        conteo[nombre] = conteo.get(nombre, 0) + cantidad

    producto_top = max(conteo, key=conteo.get) if conteo else "N/A"

    # 📦 Stock bajo
    stock_bajo = len(ProductoModel.obtener_stock_bajo())

    # 🔴 Productos críticos
    productos_criticos = len(
        [p for p in productos if p["nivel_criticidad"] == "Crítico"]
    )

    # 🟠 Productos Clase A
    productos_a = len(
        [p for p in productos if p["clasificacion_abc"] == "A"]
    )

    return jsonify({
        "ventas_totales": ventas_totales,
        "stock_bajo": stock_bajo,
        "producto_top": producto_top,
        "productos_criticos": productos_criticos,
        "productos_a": productos_a
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
        resumen[fecha] = resumen.get(fecha, 0) + v["cantidad"]

    resultado = [
        {"fecha": f, "total": t}
        for f, t in sorted(resumen.items())
    ]

    return jsonify(resultado)