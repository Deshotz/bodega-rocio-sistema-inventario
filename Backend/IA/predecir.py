import joblib
import pandas as pd
from datetime import timedelta
import numpy as np

MODEL_PATH = "Backend/IA/modelos/modelo_demanda.pkl"


def calcular_criticidad(abc, tipo, lead_time):
    """
    Sistema multicriterio de priorización estratégica
    """

    if abc == "Alta" and tipo == "perecible":
        return "🔴 Crítico"
    elif abc == "Alta":
        return "🟠 Alto"
    elif tipo == "perecible":
        return "🟡 Medio"
    else:
        return "🟢 Bajo"


def predecir_proximos_dias(producto_id: int, dias: int = 7):

    pack = joblib.load(MODEL_PATH)

    model = pack["model"]
    features = pack["features"]
    ultima_fecha = pd.to_datetime(pack["ultima_fecha"])
    tipo_map = pack["tipo_producto_map"]
    lead_map = pack["lead_time_map"]
    abc_map = pack["abc_map"]

    tipo = tipo_map.get(producto_id, "no_perecible")
    lead_time = lead_map.get(producto_id, 7)
    abc = abc_map.get(producto_id, "Baja")

    criticidad = calcular_criticidad(abc, tipo, lead_time)

    resultados = []
    fecha = ultima_fecha

    # Inicializamos memoria histórica en cero
    lag_1 = 0
    lag_7 = 0
    lag_14 = 0
    historico = []

    for _ in range(dias):

        fecha = fecha + timedelta(days=1)

        ma_7 = np.mean(historico[-7:]) if len(historico) >= 7 else 0
        ma_14 = np.mean(historico[-14:]) if len(historico) >= 14 else 0

        row = {
            "producto_id": producto_id,
            "dia_semana": fecha.dayofweek,
            "mes": fecha.month,
            "dia_mes": fecha.day,
            "semana_anio": int(fecha.isocalendar().week),
            "lag_1": lag_1,
            "lag_7": lag_7,
            "lag_14": lag_14,
            "ma_7": ma_7,
            "ma_14": ma_14,
            "lead_time": lead_time,
        }

        # Agregar columnas dummy necesarias
        for col in features:
            if col not in row:
                row[col] = 0

        X = pd.DataFrame([row])[features]

        pred = float(model.predict(X)[0])
        if pred < 0:
            pred = 0.0

        historico.append(pred)

        # Actualizamos lags dinámicamente
        lag_14 = lag_7
        lag_7 = lag_1
        lag_1 = pred

        resultados.append({
            "fecha": str(fecha.date()),
            "demanda_predicha": round(pred, 2),
            "lead_time": lead_time,
            "stock_recomendado": round(pred * lead_time, 2),
            "categoria_rotacion": abc,
            "tipo_producto": tipo,
            "nivel_criticidad": criticidad
        })

    return resultados


if __name__ == "__main__":
    print("\n===== Producto 1 (Arroz) =====")
    print(predecir_proximos_dias(1, dias=7))

    print("\n===== Producto 15 (Yogurt) =====")
    print(predecir_proximos_dias(15, dias=7))

    print("\n===== Producto 20 (Galletas Soda) =====")
    print(predecir_proximos_dias(20, dias=7))