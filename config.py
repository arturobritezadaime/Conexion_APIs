import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Clase de configuración del proyecto."""
    FRED_API_KEY = os.getenv("FRED_API_KEY")
    SERIE_INFLACION = "CPIAUCSL"
    NOMBRE_ARCHIVO = "inflacion_eeuu.xlsx"