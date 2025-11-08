import pandas as pd
import numpy as np

# RUTA DE ENTRADA Y SALIDA
FILE_PATH = 'data1/online_retail_II.csv' 
CLEAN_DATA_FILE = 'data1/cleaned_retail_data.csv' # Archivo de salida para la fase SQL

print("--- FASE DE LIMPIEZA Y TRANSFORMACIÓN (T) ---")

try:
    # 1. Carga (E)
    df = pd.read_csv(FILE_PATH, encoding='ISO-8859-1')
    initial_rows = len(df)

    # 2. Limpieza de Datos (Transformación Crítica)

    # A. Manejar Nulos Críticos (Customer ID)
    df.dropna(subset=['Customer ID'], inplace=True)

    # B. Manejar Valores Inválidos (Devoluciones/Transacciones Negativas)
    df = df[df['Quantity'] > 0]
    df = df[df['Price'] > 0]

    # C. Conversión de Tipos (CRÍTICO para cálculos)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Customer ID'] = df['Customer ID'].astype(int).astype(str)
    # Renombrar columnas para consistencia y fácil uso
    df.columns = ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'CustomerID', 'Country']

    # 3. Feature Engineering (Crear métrica de Ingreso - CRÍTICO)
    df['Total_Price'] = df['Quantity'] * df['Price']

    # 4. Resumen de la Limpieza
    rows_after_cleaning = len(df)
    print(f"Filas iniciales: {initial_rows}")
    print(f"Filas eliminadas: {initial_rows - rows_after_cleaning}")
    print(f"Filas después de la limpieza: {rows_after_cleaning}")
    print("\n--- NUEVOS TIPOS DE DATOS (Verificación final) ---")
    df.info()

    # 5. Carga de los Datos Limpios (Guardar en CSV limpio para la fase SQL)
    df.to_csv(CLEAN_DATA_FILE, index=False)
    print(f"\n✅ Datos limpios guardados en: {CLEAN_DATA_FILE}")

except Exception as e:
    print(f"❌ ERROR durante la limpieza y transformación: {e}")

print("\n--- FASE DE LIMPIEZA COMPLETADA ---")
