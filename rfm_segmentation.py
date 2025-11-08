import pandas as pd
from sqlalchemy import create_engine

# --- Configuración ---
DB_NAME = 'retail_db.sqlite'

print("--- INICIANDO HITO 4: SEGMENTACIÓN RFM ---")

try:
    # 1. CONEXIÓN Y CARGA
    engine = create_engine(f'sqlite:///{DB_NAME}')
    rfm_df = pd.read_sql_table('customer_rfm_model', engine)
    
    # 2. PUNTUACIÓN (SCORING) - Usamos rank(method='first') para robustez
    
    # R (Recencia): Asignar la puntuación 4 al cliente más reciente (valor MÍNIMO).
    # Aplicamos rank para manejar empates antes de qcut.
    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'].rank(method='first'), q=4, labels=[4, 3, 2, 1]).astype(int)
    
    # F (Frecuencia): Asignar la puntuación 4 al cliente con MAYOR frecuencia (valor MÁXIMO).
    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    
    # M (Valor Monetario): Asignar la puntuación 4 al cliente con MAYOR gasto (valor MÁXIMO).
    rfm_df['M_Score'] = pd.qcut(rfm_df['MonetaryValue'].rank(method='first'), q=4, labels=[1, 2, 3, 4]).astype(int)
    
    # 3. COMBINACIÓN DE PUNTUACIONES
    
    # Creamos una puntuación combinada (ej. 444 = Campeón)
    rfm_df['RFM_Score_Total'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
    
    # 4. ASIGNACIÓN DE SEGMENTOS DE NEGOCIO (FUNCIÓN CLAVE)
    
    # Definimos la función para asignar etiquetas claras (segmentos de negocio) basadas en el score
    def assign_rfm_segment(df):
        # 444: Champions
        if df['R_Score'] == 4 and df['F_Score'] == 4 and df['M_Score'] == 4:
            return '01 - Champions'
        # R = 4 (Reciente) y F/M alto: Potential Loyalists
        elif df['R_Score'] == 4 and df['F_Score'] >= 3 and df['M_Score'] >= 3:
            return '02 - Potential Loyalists'
        # F/M alto, R decayendo: Loyal Customers
        elif df['R_Score'] >= 2 and df['F_Score'] >= 3 and df['M_Score'] >= 3:
            return '03 - Loyal Customers'
        # R bajo, F/M bajo: At Risk (necesitan reactivación)
        elif df['R_Score'] <= 2 and df['F_Score'] <= 2 and df['M_Score'] <= 2:
            return '04 - At Risk'
        # R bajo, F/M muy bajo: Lost Customers
        elif df['R_Score'] == 1 and df['F_Score'] == 1 and df['M_Score'] == 1:
            return '05 - Lost Customers'
        # Otros
        else:
            return '06 - Others / Need Attention'
            
    rfm_df['RFM_Segment'] = rfm_df.apply(assign_rfm_segment, axis=1)

    # 5. CARGA DEL MODELO FINAL
    
    # Cargar la tabla segmentada de nuevo a la base de datos
    rfm_df.to_sql('customer_segmentation_model', engine, if_exists='replace', index=False)
    
    print("El modelo de Segmentación RFM ha sido completado y cargado en la tabla 'customer_segmentation_model'.")

    # 6. VERIFICACIÓN
    
    print("\n--- EJEMPLO DE CLIENTES CON PUNTUACIONES Y SEGMENTOS ---")
    print(rfm_df[['CustomerID', 'R_Score', 'F_Score', 'M_Score', 'RFM_Score_Total', 'RFM_Segment']].head(10))
    
    print("\n--- DISTRIBUCIÓN DE SEGMENTOS DE NEGOCIO ---")
    print(rfm_df['RFM_Segment'].value_counts())

except Exception as e:
    print(f"ERROR durante la Segmentación RFM: {e}")

print("\n--- HITO 4 COMPLETADO ---")
