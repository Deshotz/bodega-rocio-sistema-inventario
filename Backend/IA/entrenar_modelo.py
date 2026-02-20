import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

RUTA_DATASET = "dataset_demanda.csv"
OUTPUT_DIR = "Backend/IA/modelos"
MODEL_PATH = os.path.join(OUTPUT_DIR, "modelo_demanda.pkl")


# =========================================================
# PREPARACIÓN DE DATOS
# =========================================================
def preparar_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df["fecha"] = pd.to_datetime(df["fecha"])

    daily = (
        df.groupby([df["producto_id"], df["producto"], df["fecha"].dt.date])["cantidad"]
        .sum()
        .reset_index()
        .rename(columns={"fecha": "fecha_dia", "cantidad": "demanda"})
    )

    daily["fecha_dia"] = pd.to_datetime(daily["fecha_dia"])

    # Variables temporales
    daily["dia_semana"] = daily["fecha_dia"].dt.dayofweek
    daily["mes"] = daily["fecha_dia"].dt.month
    daily["dia_mes"] = daily["fecha_dia"].dt.day
    daily["semana_anio"] = daily["fecha_dia"].dt.isocalendar().week.astype(int)

    # Orden temporal
    daily = daily.sort_values(["producto_id", "fecha_dia"]).reset_index(drop=True)

    # Lags
    for lag in [1, 7, 14]:
        daily[f"lag_{lag}"] = daily.groupby("producto_id")["demanda"].shift(lag)

    # Promedios móviles
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

    return daily


# =========================================================
# SPLIT TEMPORAL
# =========================================================
def split_temporal(daily: pd.DataFrame):
    daily = daily.sort_values("fecha_dia").reset_index(drop=True)
    cut = int(len(daily) * 0.8)

    train = daily.iloc[:cut].copy()
    test = daily.iloc[cut:].copy()

    return train, test


# =========================================================
# ENTRENAMIENTO
# =========================================================
def entrenar():
    if not os.path.exists(RUTA_DATASET):
        raise FileNotFoundError(f"No existe {RUTA_DATASET}. Genera el dataset primero.")

    df = pd.read_csv(RUTA_DATASET)
    required = {"producto_id", "producto", "cantidad", "fecha"}

    if not required.issubset(df.columns):
        raise ValueError(f"El CSV debe tener columnas: {required}. Tienes: {df.columns}")

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
    ]

    X_train = train[features]
    y_train = train["demanda"]
    X_test = test[features]
    y_test = test["demanda"]

    # ==============================
    # BASELINE (MA_7)
    # ==============================
    baseline_pred = test["ma_7"].values
    baseline_mae = mean_absolute_error(y_test, baseline_pred)
    baseline_rmse = np.sqrt(mean_squared_error(y_test, baseline_pred))
    baseline_r2 = r2_score(y_test, baseline_pred)

    # ==============================
    # RANDOM FOREST MEJORADO
    # ==============================
    model = RandomForestRegressor(
        n_estimators=600,
        random_state=42,
        max_depth=15,
        min_samples_split=4,
        min_samples_leaf=1,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)

    # MAPE
    mape = np.mean(np.abs((y_test - pred) / (y_test + 1e-5))) * 100

    # ==============================
    # IMPORTANCIA DE VARIABLES
    # ==============================
    importancias = model.feature_importances_

    print("\n🔎 Importancia de variables:")
    for f, imp in sorted(zip(features, importancias), key=lambda x: x[1], reverse=True):
        print(f"{f}: {imp:.4f}")

    # ==============================
    # GUARDAR MODELO + MÉTRICAS
    # ==============================
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    joblib.dump(
        {
            "model": model,
            "features": features,
            "ultima_fecha": daily["fecha_dia"].max(),
            "productos": daily[
                ["producto_id", "producto"]
            ].drop_duplicates().sort_values("producto_id").to_dict("records"),
            "metricas": {
                "baseline": {
                    "mae": baseline_mae,
                    "rmse": baseline_rmse,
                    "r2": baseline_r2
                },
                "random_forest": {
                    "mae": mae,
                    "rmse": rmse,
                    "r2": r2,
                    "mape": mape
                }
            }
        },
        MODEL_PATH
    )

    # ==============================
    # RESULTADOS
    # ==============================
    print("\n✅ Entrenamiento terminado")
    print(f"\n📌 Baseline (MA_7)")
    print(f"MAE: {baseline_mae:.3f}")
    print(f"RMSE: {baseline_rmse:.3f}")
    print(f"R²: {baseline_r2:.3f}")

    print(f"\n🤖 RandomForest Mejorado")
    print(f"MAE: {mae:.3f}")
    print(f"RMSE: {rmse:.3f}")
    print(f"R²: {r2:.3f}")
    print(f"MAPE: {mape:.2f}%")

    print(f"\n💾 Modelo guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    entrenar()
