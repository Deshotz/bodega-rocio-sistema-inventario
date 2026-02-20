import pandas as pd
from Backend.Modelo.db import get_connection

def exportar_dataset():
    conn = get_connection()

    query = """
    SELECT 
        v.id,
        v.producto_id,
        p.nombre AS producto,
        v.cantidad,
        v.fecha
    FROM ventas v
    JOIN productos p ON v.producto_id = p.id
    ORDER BY v.fecha ASC
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df.to_csv("dataset_demanda.csv", index=False, encoding="utf-8-sig")
    print("✅ Dataset generado: dataset_demanda.csv")

if __name__ == "__main__":
    exportar_dataset()
