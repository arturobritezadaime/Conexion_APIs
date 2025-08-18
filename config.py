import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Clase de configuración del proyecto."""
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    SERIE_INFLACION = "CPIAUCSL"  # Índice de Precios al Consumidor (IPC)
    SERIE_PIB = "GDP"  # Producto Interno Bruto (trimestral, en miles de millones de USD)
    SERIE_TASA_INTERES = "FEDFUNDS"  # Tasa de fondos federales (mensual, %)
    SERIE_DESEMPLEO = "UNRATE"  # Tasa de desempleo (mensual, %)
    NOMBRE_ARCHIVO_INFLACION = "inflacion_eeuu.xlsx"
    NOMBRE_ARCHIVO_PIB = "pib_eeuu.xlsx"
    NOMBRE_ARCHIVO_TASA_INTERES = "tasas_interes_eeuu.xlsx"
    NOMBRE_ARCHIVO_DESEMPLEO = "desempleo_eeuu.xlsx"