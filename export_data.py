import sqlite3
import pandas as pd
import os

DB_NAME = 'retail_db.sqlite'
OUTPUT_DIR = 'data_for_bi'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'customer_segmentation_ready.csv')
TABLE_NAME = 'customer_segmentation_model'

print("--- EXPORTACIÓN DE DATOS - POWER BI ---")

try:
    # 1. Conexión a la base de datos
    conn = sqlite3.connect(DB_NAME)

    # 2. Consulta de la tabla final
    # Seleccionamos la tabla que contiene las métricas RFM y los segmentos de negocio
    query = f"SELECT * FROM {TABLE_NAME};"
    df_export = pd.read_sql_query(query, conn)
    
    conn.close()
    
    # 3. Guardar como CSV
    # Crea el directorio 'data_for_bi' si no existe (Buena Práctica)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Exporta el DataFrame final a CSV, sin incluir el índice de Pandas
    df_export.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Datos exportados con éxito al archivo: {OUTPUT_FILE}")
    print(f"Filas exportadas: {len(df_export)}")

except Exception as e:
    print(f"ERROR durante la exportación de datos: {e}")

print("--- EXPORTACIÓN COMPLETADA ---")
