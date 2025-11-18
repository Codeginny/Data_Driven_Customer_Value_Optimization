import pandas as pd
from sqlalchemy import create_engine

# --- Configuración ---
DB_NAME = 'retail_db.sqlite'

print("--- INICIANDO HITO 4: SEGMENTACIÓN RFM ---")

try:
    # 1. CONEXIÓN Y CARGA
    engine = create_engine(f'sqlite:///{DB_NAME}')
    # Asegúrate de que customer_rfm_model ya incluye las correcciones de CustomerID (string) y MonetaryValue (rounded)
    rfm_df = pd.read_sql_table('customer_rfm_model', engine)
    
    # 2. PUNTUACIÓN (SCORING) - Usamos rank(method='first') para robustez
    
    # R (Recencia): Asignar la puntuación 4 al cliente más reciente (valor MÍNIMO).
    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'].rank(method='first'), q=4, labels=[4, 3, 2, 1]).astype(int)
    
    # F (Frecuencia): Asignar la puntuación 4 al cliente con MAYOR frecuencia (valor MÁXIMO).
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    
    # M (Valor Monetario): Asignar la puntuación 4 al cliente con MAYOR gasto (valor MÁXIMO).
    rfm_df['M_Score'] = pd.qcut(rfm_df['MonetaryValue'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    
    # 3. COMBINACIÓN DE PUNTUACIONES
    
    rfm_df['RFM_Score_Total'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
    
    # 4. ASIGNACIÓN DE SEGMENTOS DE NEGOCIO (FUNCIÓN CLAVE)
    
    def assign_rfm_segment(df):
        if df['R_Score'] == 4 and df['F_Score'] == 4 and df['M_Score'] == 4:
            return '01 - Champions'
        elif df['R_Score'] == 4 and df['F_Score'] >= 3 and df['M_Score'] >= 3:
            return '02 - Potential Loyalists'
        elif df['R_Score'] >= 2 and df['F_Score'] >= 3 and df['M_Score'] >= 3:
            return '03 - Loyal Customers'
        elif df['R_Score'] <= 2 and df['F_Score'] <= 2 and df['M_Score'] <= 2:
            return '04 - At Risk'
        elif df['R_Score'] == 1 and df['F_Score'] == 1 and df['M_Score'] == 1:
            return '05 - Lost Customers'
        else:
            return '06 - Others / Need Attention'

    rfm_df['RFM_Segment'] = rfm_df.apply(assign_rfm_segment, axis=1)

    # CRÍTICO: Solución de Consistencia. Elimina espacios en blanco para Power BI.
    rfm_df['RFM_Segment'] = rfm_df['RFM_Segment'].str.strip() 

    # 5. CARGA DEL MODELO FINAL
    
    rfm_df.to_sql('customer_segmentation_model', engine, if_exists='replace', index=False)
    
    print("El modelo de Segmentación RFM ha sido completado y cargado en la tabla 'customer_segmentation_model'.")

    # 6. VERIFICACIÓN
    print("\n--- DISTRIBUCIÓN DE SEGMENTOS DE NEGOCIO ---")
    print(rfm_df['RFM_Segment'].value_counts()) # Se movió para que muestre la distribución

except Exception as e:
    print(f"ERROR durante la Segmentación RFM: {e}")

print("\n--- HITO 4 COMPLETADO ---")
