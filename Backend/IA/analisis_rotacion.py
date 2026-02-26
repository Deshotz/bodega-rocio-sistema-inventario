import pandas as pd

# 1️⃣ Cargar dataset
df = pd.read_csv("../../dataset_demanda.csv")

# 2️⃣ Convertir fecha a datetime
df["fecha"] = pd.to_datetime(df["fecha"])

# 3️⃣ Agrupar por producto
rotacion = df.groupby(["producto_id", "producto"]).agg(
    total_vendido=("cantidad", "sum"),
    dias_con_venta=("fecha", "nunique"),
    promedio_diario=("cantidad", "mean"),
    desviacion=("cantidad", "std"),
    frecuencia=("cantidad", "count")
).reset_index()

# 4️⃣ Ordenar por total vendido (mayor a menor)
rotacion = rotacion.sort_values(by="total_vendido", ascending=False)

# 5️⃣ Mostrar resultados
print("\n📊 ANÁLISIS DE ROTACIÓN POR PRODUCTO\n")
print(rotacion)

# 6️⃣ Guardar análisis
rotacion.to_csv("analisis_rotacion.csv", index=False)

print("\n✅ Archivo 'analisis_rotacion.csv' generado correctamente.")

# 7️⃣ Clasificación ABC según total vendido
rotacion["porcentaje_acumulado"] = (
    rotacion["total_vendido"].cumsum() / rotacion["total_vendido"].sum()
)

def clasificar_abc(p):
    if p <= 0.70:
        return "Alta"
    elif p <= 0.90:
        return "Media"
    else:
        return "Baja"

rotacion["categoria_rotacion"] = rotacion["porcentaje_acumulado"].apply(clasificar_abc)

print("\n📊 CLASIFICACIÓN ABC\n")
print(rotacion[["producto", "total_vendido", "categoria_rotacion"]])

# Guardar nuevamente
rotacion.to_csv("analisis_rotacion.csv", index=False)