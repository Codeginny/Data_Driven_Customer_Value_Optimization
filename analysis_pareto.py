import sqlite3
import pandas as pd

DB_NAME = 'retail_db.sqlite'

print("--- INICIANDO ANÁLISIS DE NEGOCIO (PARETO) ---")

try:
    # 1. Conexión a la base de datos
    conn = sqlite3.connect(DB_NAME)

    # 2. Consulta de Negocio: Clientes Top 10 por Valor Monetario (M)
    query_top_value = """
    SELECT 
        CustomerID, 
        MonetaryValue 
    FROM 
        customer_rfm_model 
    ORDER BY 
        MonetaryValue DESC 
    LIMIT 10;
    """
    
    print("\n--- TOP 10 CLIENTES POR VALOR MONETARIO ---")
    top_10_df = pd.read_sql_query(query_top_value, conn)
    print(top_10_df)

    # 3. Análisis de Pareto (Regla 80/20) - CRÍTICO
    # a. Cálculo del Ingreso Total
    total_revenue_query = "SELECT SUM(MonetaryValue) FROM customer_rfm_model;"
    total_revenue = pd.read_sql_query(total_revenue_query, conn).iloc[0, 0]

    # b. Obtener el número de clientes para el Top 20%
    total_customers_query = "SELECT COUNT(CustomerID) FROM customer_rfm_model;"
    total_customers = pd.read_sql_query(total_customers_query, conn).iloc[0, 0]
    
    top_20_percent_count = int(total_customers * 0.20)
    
    # c. Calcular el Ingreso del Top 20%
    top_20_percent_revenue_query = f"""
    SELECT SUM(MonetaryValue) AS Top20Revenue
    FROM (
        SELECT MonetaryValue
        FROM customer_rfm_model
        ORDER BY MonetaryValue DESC
        LIMIT {top_20_percent_count}
    );
    """
    top_20_revenue = pd.read_sql_query(top_20_percent_revenue_query, conn).iloc[0, 0]
    
    # d. Presentar los resultados
    print("\n--- ANÁLISIS DE PARETO (REGLA 80/20) ---")
    print(f"Total Revenue: {total_revenue:,.2f}")
    print(f"Revenue from Top 20% Customers: {top_20_revenue:,.2f}")
    print(f"Percentage of Revenue from Top 20% Customers: {(top_20_revenue / total_revenue) * 100:.2f}%")

    conn.close()

except Exception as e:
    print(f"ERROR durante el Análisis de Pareto: {e}")

print("\n--- ANÁLISIS DE NEGOCIO COMPLETADO ---")
