import pandas as pd
from fredapi import Fred
from config import Config

def obtener_datos_inflacion(api_key: str, serie: str) -> pd.DataFrame:
    """Descarga y procesa los datos del IPC desde FRED."""
    try:
        fred = Fred(api_key=api_key)
        data = fred.get_series(serie)
        if data is None:
            raise ValueError(f"No se pudieron obtener datos para la serie: {serie}")
        
        df = pd.DataFrame(data, columns=["CPI"])
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"❌ Error al conectar o obtener datos de FRED: {e}")
        return None

def calcular_inflacion(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la inflación mensual y acumulada."""
    df_procesado = df.copy()
    
    # Calcular inflación mensual (%) y redondear
    df_procesado["Inflacion_Mensual"] = (df_procesado["CPI"].pct_change() * 100).round(2)
    
    # Filtrar últimos 3 años
    fecha_inicio = df_procesado.index.max() - pd.DateOffset(years=3)
    df_3y = df_procesado.loc[df_procesado.index >= fecha_inicio].copy()
    
    # Crear columnas de año y mes
    df_3y.loc[:, "Año"] = df_3y.index.year
    df_3y.loc[:, "Mes"] = df_3y.index.month
    
    # Calcular inflación acumulada del año y redondear
    df_3y.loc[:, "Inflacion_Acumulada_Año"] = df_3y.groupby("Año")["Inflacion_Mensual"].cumsum().round(2)
    
    # Formatear mes con dos dígitos
    df_3y.loc[:, "Mes"] = df_3y["Mes"].apply(lambda x: f"{x:02d}")
    
    # Crear columna Año-Mes
    df_3y.loc[:, "Año-Mes"] = df_3y["Año"].astype(str) + "-" + df_3y["Mes"]
    
    # Reorganizar columnas finales
    df_final = df_3y[["Año-Mes", "Inflacion_Mensual", "Inflacion_Acumulada_Año"]].reset_index(drop=True)
    
    return df_final

def guardar_a_excel(df: pd.DataFrame, nombre_archivo: str):
    """Guarda el DataFrame en un archivo de Excel."""
    try:
        df.to_excel(nombre_archivo, index=False, engine="openpyxl")
        print(f"✅ Archivo guardado como {nombre_archivo}")
    except ImportError:
        print("❌ Error: 'openpyxl' no está instalado. Por favor, instálalo con 'pip install openpyxl'.")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")

def main():
    """Función principal para ejecutar el script."""
    api_key = Config.FRED_API_KEY
    if not api_key:
        print("❌ Error: No se encontró la clave de la API. Asegúrate de que tu archivo .env está configurado correctamente.")
        return

    serie = Config.SERIE_INFLACION
    
    df_completo = obtener_datos_inflacion(api_key, serie)
    if df_completo is not None:
        df_final = calcular_inflacion(df_completo)
        
        print("---")
        print("Últimos meses:")
        print(df_final.tail(12))
        print("---")
        
        guardar_a_excel(df_final, Config.NOMBRE_ARCHIVO)

if __name__ == "__main__":
    main()