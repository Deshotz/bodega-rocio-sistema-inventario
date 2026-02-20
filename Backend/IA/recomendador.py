import joblib
import pandas as pd
from datetime import datetime, timedelta

modelo = joblib.load("Backend/IA/modelos/modelo_demanda.pkl")


def recomendar_reabastecimiento(dias=7):

    fechas = pd.date_range(
        start=datetime.today(),
        periods=dias
    )

    X = pd.DataFrame({
        "dia_semana": fechas.dayofweek,
        "mes": fechas.month,
        "dia_mes": fechas.day
    })

    pred = modelo.predict(X)

    demanda_total = int(sum(pred))

    # 🔒 Stock mínimo sugerido
    stock_actual = 500  # luego lo hacemos dinámico

    if demanda_total > stock_actual:
        comprar = demanda_total - stock_actual
    else:
        comprar = 0

    return {
        "demanda_estimada": demanda_total,
        "stock_actual": stock_actual,
        "recomendacion_compra": comprar
    }
