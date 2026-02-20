import joblib
import pandas as pd
from datetime import timedelta
import os

MODEL_PATH = "Backend/IA/modelos/modelo_demanda.pkl"

def predecir_proximos_dias(producto_id: int, dias: int = 7):
    pack = joblib.load(MODEL_PATH)
    model = pack["model"]
    features = pack["features"]
    ultima_fecha = pd.to_datetime(pack["ultima_fecha"])

    # Para una predicción real, necesitamos lags y promedios.
    # En esta versión simple (para demo + rubrica), asumimos lags=0 si no se pasan.
    # Luego lo mejoramos leyendo histórico por producto desde DB.
    resultados = []
    fecha = ultima_fecha

    lag_1 = 0
    lag_7 = 0
    lag_14 = 0
    ma_7 = 0
    ma_14 = 0

    for _ in range(dias):
        fecha = fecha + timedelta(days=1)
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
        }
        X = pd.DataFrame([row])[features]
        pred = float(model.predict(X)[0])
        if pred < 0:
            pred = 0.0
        resultados.append({"fecha": str(fecha.date()), "demanda_predicha": round(pred, 2)})

    return resultados

if __name__ == "__main__":
    print(predecir_proximos_dias(1, dias=7))
