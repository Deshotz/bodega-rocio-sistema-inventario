import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

RUTA_DATASET = "dataset_demanda.csv"
OUTPUT_DIR = "Backend/IA/modelos"
MODEL_PATH = os.path.join(OUTPUT_DIR, "modelo_demanda.pkl")

# --------------------------------------------------
# CLASIFICACIÓN LOGÍSTICA
# --------------------------------------------------

TIPO_PRODUCTO = {
    15: "perecible",
    16: "perecible",
    17: "perecible",
    18: "perecible",

    14: "semi",
    27: "semi",
    28: "semi",
    29: "semi",
    30: "semi",
}

LEAD_TIME = {
    15: 2,
    16: 2,
    17: 2,
    18: 1,

    14: 3,
    27: 3,
    28: 3,
    29: 4,
    30: 3,
}

# --------------------------------------------------
# CLASIFICACIÓN ABC (según tu análisis_rotacion.csv)
# --------------------------------------------------

ABC_MAP = {
    12: "Alta", 1: "Alta", 39: "Alta", 29: "Alta", 2: "Alta", 5: "Alta",
    10: "Alta", 24: "Alta", 34: "Alta", 16: "Alta", 15: "Alta", 22: "Alta",
    8: "Alta", 6: "Alta", 38: "Alta", 18: "Alta", 28: "Alta", 30: "Alta",
    4: "Alta", 3: "Alta", 9: "Alta", 23: "Alta", 26: "Alta", 17: "Alta",

    7: "Media", 11: "Media", 40: "Media", 31: "Media",
    33: "Media", 14: "Media", 13: "Media", 36: "Media", 35: "Media",

    20: "Baja", 19: "Baja", 25: "Baja", 27: "Baja",
    32: "Baja", 21: "Baja", 37: "Baja", 41: "Baja",
}

# --------------------------------------------------
# PREPARACIÓN DEL DATASET
# --------------------------------------------------

def preparar_dataset(df: pd.DataFrame) -> pd.DataFrame:

    df["fecha"] = pd.to_datetime(df["fecha"])

    daily = (
        df.groupby([df["producto_id"], df["producto"], df["fecha"].dt.date])["cantidad"]
        .sum()
        .reset_index()
        .rename(columns={"fecha": "fecha_dia", "cantidad": "demanda"})
    )

    daily["fecha_dia"] = pd.to_datetime(daily["fecha_dia"])

    # Features temporales
    daily["dia_semana"] = daily["fecha_dia"].dt.dayofweek
    daily["mes"] = daily["fecha_dia"].dt.month
    daily["dia_mes"] = daily["fecha_dia"].dt.day
    daily["semana_anio"] = daily["fecha_dia"].dt.isocalendar().week.astype(int)

    daily = daily.sort_values(["producto_id", "fecha_dia"]).reset_index(drop=True)

    # Lags
    for lag in [1, 7, 14]:
        daily[f"lag_{lag}"] = daily.groupby("producto_id")["demanda"].shift(lag)

    # Medias móviles
    daily["ma_7"] = (
        daily.groupby("producto_id")["demanda"]
        .shift(1)
        .rolling(7)
        .mean()
        .reset_index(level=0, drop=True)
    )

    daily["ma_14"] = (
        daily.groupby("producto_id")["demanda"]
        .shift(1)
        .rolling(14)
        .mean()
        .reset_index(level=0, drop=True)
    )

    daily[["lag_1", "lag_7", "lag_14", "ma_7", "ma_14"]] = daily[
        ["lag_1", "lag_7", "lag_14", "ma_7", "ma_14"]
    ].fillna(0)

    # --------------------------------------------------
    # VARIABLES LOGÍSTICAS
    # --------------------------------------------------

    daily["tipo_producto"] = daily["producto_id"].map(TIPO_PRODUCTO).fillna("no_perecible")
    daily["lead_time"] = daily["producto_id"].map(LEAD_TIME).fillna(7)
    daily["categoria_rotacion"] = daily["producto_id"].map(ABC_MAP).fillna("Baja")

    daily = pd.get_dummies(daily, columns=["tipo_producto", "categoria_rotacion"], drop_first=True)

    return daily


# --------------------------------------------------
# SPLIT TEMPORAL
# --------------------------------------------------

def split_temporal(daily: pd.DataFrame):
    daily = daily.sort_values("fecha_dia").reset_index(drop=True)
    cut = int(len(daily) * 0.8)

    train = daily.iloc[:cut].copy()
    test = daily.iloc[cut:].copy()

    return train, test


# --------------------------------------------------
# ENTRENAMIENTO
# --------------------------------------------------

def entrenar():

    df = pd.read_csv(RUTA_DATASET)

    daily = preparar_dataset(df)
    train, test = split_temporal(daily)

    features = [
        "producto_id",
        "dia_semana",
        "mes",
        "dia_mes",
        "semana_anio",
        "lag_1",
        "lag_7",
        "lag_14",
        "ma_7",
        "ma_14",
        "lead_time",
    ] + [col for col in daily.columns if "tipo_producto_" in col or "categoria_rotacion_" in col]

    X_train = train[features]
    y_train = train["demanda"]
    X_test = test[features]
    y_test = test["demanda"]

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "features": features,
            "ultima_fecha": daily["fecha_dia"].max(),
            "productos": daily[["producto_id", "producto"]]
                .drop_duplicates()
                .sort_values("producto_id")
                .to_dict("records"),
            "tipo_producto_map": TIPO_PRODUCTO,
            "lead_time_map": LEAD_TIME,
            "abc_map": ABC_MAP,
        },
        MODEL_PATH
    )

    print("✅ Entrenamiento terminado")
    print(f"🤖 RandomForest -> MAE: {mae:.3f} | RMSE: {rmse:.3f}")
    print(f"💾 Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    entrenar()