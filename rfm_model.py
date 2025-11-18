import pandas as pd
from sqlalchemy import create_engine

# Rutas y conexión a la base de datos
CLEAN_DATA_FILE = 'data1/cleaned_retail_data.csv'
DB_NAME = 'retail_db.sqlite'

# La fecha de referencia debe ser posterior a la última transacción (2011-12-09).
REFERENCE_DATE = pd.to_datetime('2012-01-01')

print("--- FASE DE MODELADO SQL (Cálculo RFM) ---")

try:
    # A. Carga de datos limpios
    df = pd.read_csv(CLEAN_DATA_FILE)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # B. Creación de la Conexión con SQL (SQLite)
    engine = create_engine(f'sqlite:///{DB_NAME}')
    
    # C. Cálculo de Métricas RFM
    
    # 1. Agregación de transacciones para calcular RFM
    rfm_df = df.groupby('CustomerID').agg(
        # Recencia: Días desde la última compra
        Recency=('InvoiceDate', lambda x: (REFERENCE_DATE - x.max()).days),
        
        # Frecuencia: Número total de transacciones (conteo de facturas únicas)
        Frequency=('Invoice', 'nunique'),
        
        # Valor Monetario: Suma de los ingresos (Total_Price)
        Monetary=('Total_Price', 'sum')
    )
    
    rfm_df.reset_index(inplace=True)
    rfm_df.rename(columns={'Monetary': 'MonetaryValue'}, inplace=True)
    
    # CRÍTICO 1: Solución de Precisión. Redondea el Valor Monetario a 2 decimales para Power BI.
    rfm_df['MonetaryValue'] = rfm_df['MonetaryValue'].round(2) 

    # CRÍTICO 2: Solución de Tipo. Convierte CustomerID a Texto para evitar agregaciones erróneas en BI.
    rfm_df['CustomerID'] = rfm_df['CustomerID'].astype(str)
    
    print("Métricas RFM calculadas con éxito.")
    
    # D. Carga del Modelo RFM en una tabla SQL separada
    rfm_df.to_sql('customer_rfm_model', engine, if_exists='replace', index=False)
    print("Modelo RFM cargado en la tabla 'customer_rfm_model' de la base de datos.")
    
    # E. Verificar el contenido del modelo RFM (Las primeras 5 filas)
    print("\n--- PRIMEROS REGISTROS DEL MODELO RFM ---")
    print(rfm_df.head())

except FileNotFoundError:
    print(f"ERROR: No se encontró el archivo de datos limpios en la ruta: {CLEAN_DATA_FILE}. Ejecute etl_profiling.py primero.")
except Exception as e:
    print(f"ERROR durante el modelado SQL/RFM: {e}")

print("\n--- FASE DE MODELADO COMPLETADA ---")
