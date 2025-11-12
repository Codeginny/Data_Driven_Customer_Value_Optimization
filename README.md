# Data-Driven Customer Value Optimization (Análisis de Valor de Cliente)

## Resumen Ejecutivo

Este proyecto establece un pipeline de análisis para optimizar la rentabilidad del cliente y las estrategias de retención en una plataforma de comercio electrónico. El objetivo principal fue segmentar la base de clientes por valor para permitir estrategias de marketing enfocadas.

**Impacto del Análisis (Conclusión para la Gerencia):**

| Métrica | Resultado | Implicación Estratégica |
| :--- | :--- | :--- |
| **Análisis de Pareto (80/20)** | El **20%** de los clientes genera el **77.24%** del Ingreso Total. | **CRÍTICO:** Las estrategias de retención deben enfocarse desproporcionadamente en este Top 20% para asegurar la rentabilidad. |
| **Segmentación RFM** | Clientes categorizados en segmentos accionables como **'Champions'** y **'At Risk'**. | Permite al equipo de Marketing dirigir campañas específicas (ej., ofertas de reactivación para el segmento 'At Risk'). |

---

## Stack Tecnológico Implementado

Este proyecto demuestra el dominio del flujo de trabajo de análisis de datos de principio a fin, utilizando herramientas valoradas por reclutadores en roles de Finanzas/Tech:

* **Lenguajes:** Python (Pandas), SQL (SQLite).
* **Modelado y Análisis:** Modelo RFM (Recencia, Frecuencia, Valor Monetario), Análisis de Pareto, Segmentación por Cuantiles.
* **Ingeniería de Datos:** Creación de un pipeline modular (ETL, Modelado, Exportación), Control de versiones (Git/GitHub), Gestión de entorno virtual (`venv`).
* **Visualización (Entrega Final):** Archivo CSV final listo para importación en **Power BI** (Hito 5).

---

##  Flujo del Pipeline de Datos

El pipeline se ejecuta secuencialmente a través de scripts modulares:

1.  **`etl_profiling.py`**: Limpieza de datos brutos. Elimina registros incompletos (e.g., sin `CustomerID`) y devoluciones (`Quantity <= 0`).
2.  **`rfm_model.py`**: Modelado. Calcula Recencia, Frecuencia y Valor Monetario (M) para cada cliente y carga el resultado en la tabla SQL `customer_rfm_model`.
3.  **`analysis_pareto.py`**: Análisis de Negocio. Ejecuta consultas SQL contra el modelo RFM para cuantificar la Regla 80/20.
4.  **`rfm_segmentation.py`**: Segmentación. Asigna una puntuación (1-4) a cada métrica RFM y etiqueta a cada cliente con un segmento de negocio (`Champions`, `At Risk`, etc.).
5.  **`export_data.py`**: Exportación final. Lee la tabla segmentada y genera el CSV final (`customer_segmentation_ready.csv`) para la visualización en BI.

---

##  Resultados de la Segmentación RFM

La segmentación divide a los clientes en grupos estratégicos:

| Segmento RFM | Definición (R_Score, F_Score, M_Score) | Implicación Estratégica (Acción) |
| :--- | :--- | :--- |
| **01 - Champions** | 444 (Reciente, Frecuente, Alto Gasto) | Recompensa y Fidelización. Pídeles referencias. |
| **04 - At Risk** | R bajo, F/M bajo (e.g., 211, 222) | Campañas de Reactivación Urgente. |
| **03 - Loyal Customers** | F/M alto, R medio (e.g., 344, 333) | Programas de Lealtad y Prevención de Abandono. |
| **05 - Lost Customers** | 111 (No compra hace mucho, solo compró una vez, gasto bajo) | Ofertas agresivas de Retorno o abandono de la inversión. |

---

**Instrucciones de Reproducción:**

1.  Clonar el repositorio: `git clone [URL]`
2.  Instalar dependencias: `pip install -r requirements.txt`
3.  Ejecutar scripts secuencialmente: `python etl_profiling.py`, `python rfm_model.py`, etc.
