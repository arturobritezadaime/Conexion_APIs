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
    
    # Filtrar últimos 3 años
    fecha_inicio = df_procesado.index.max() - pd.DateOffset(years=3)
    df_3y = df_procesado.loc[df_procesado.index >= fecha_inicio].copy()
    
    # Calcular inflación mensual (%) y redondear
    df_3y["Inflacion_Mensual"] = (df_3y["CPI"].pct_change() * 100).round(2)
    
    # Crear columnas de año y mes
    df_3y.loc[:, "Año"] = df_3y.index.year
    df_3y.loc[:, "Mes"] = df_3y.index.month.astype(str)
    
    # Calcular inflación acumulada del año y redondear
    df_3y.loc[:, "Inflacion_Acumulada_Año"] = df_3y.groupby("Año")["Inflacion_Mensual"].cumsum().round(2)
    
    # Formatear mes con dos dígitos
    df_3y.loc[:, "Mes"] = df_3y["Mes"].apply(lambda x: f"{int(x):02d}")
    
    # Crear columna Año-Mes
    df_3y.loc[:, "Año-Mes"] = df_3y["Año"].astype(str) + "-" + df_3y["Mes"]
    
    # Reorganizar columnas finales
    df_final = df_3y[["Año-Mes", "Inflacion_Mensual", "Inflacion_Acumulada_Año"]].reset_index(drop=True)
    
    return df_final

def obtener_datos_pib(api_key: str, serie: str) -> pd.DataFrame:
    """Descarga y procesa los datos del PIB desde FRED."""
    try:
        fred = Fred(api_key=api_key)
        data = fred.get_series(serie)
        if data is None:
            raise ValueError(f"No se pudieron obtener datos para la serie: {serie}")
        
        df = pd.DataFrame(data, columns=["PIB"])
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"❌ Error al conectar o obtener datos de FRED: {e}")
        return None

def calcular_pib(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula el crecimiento trimestral del PIB."""
    df_procesado = df.copy()
    
    # Filtrar últimos 3 años
    fecha_inicio = df_procesado.index.max() - pd.DateOffset(years=3)
    df_3y = df_procesado.loc[df_procesado.index >= fecha_inicio].copy()
    
    # Calcular crecimiento trimestral (%) y redondear
    df_3y["Crecimiento_Trimestral"] = (df_3y["PIB"].pct_change() * 100).round(2)
    
    # Crear columnas de año y trimestre
    df_3y.loc[:, "Año"] = df_3y.index.year
    df_3y.loc[:, "Trimestre"] = df_3y.index.quarter.astype(str)
    
    # Formatear trimestre con dos dígitos
    df_3y.loc[:, "Trimestre"] = df_3y["Trimestre"].apply(lambda x: f"Q{int(x):01d}")
    
    # Crear columna Año-Trimestre
    df_3y.loc[:, "Año-Trimestre"] = df_3y["Año"].astype(str) + "-" + df_3y["Trimestre"]
    
    # Reorganizar columnas finales
    df_final = df_3y[["Año-Trimestre", "PIB", "Crecimiento_Trimestral"]].reset_index(drop=True)
    
    return df_final

def obtener_datos_tasa_interes(api_key: str, serie: str) -> pd.DataFrame:
    """Descarga y procesa los datos de la tasa de fondos federales desde FRED."""
    try:
        fred = Fred(api_key=api_key)
        data = fred.get_series(serie)
        if data is None:
            raise ValueError(f"No se pudieron obtener datos para la serie: {serie}")
        
        df = pd.DataFrame(data, columns=["Tasa_Interes"])
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"❌ Error al conectar o obtener datos de FRED: {e}")
        return None

def procesar_tasa_interes(df: pd.DataFrame) -> pd.DataFrame:
    """Procesa los datos de tasas de interés."""
    df_procesado = df.copy()
    
    # Filtrar últimos 3 años
    fecha_inicio = df_procesado.index.max() - pd.DateOffset(years=3)
    df_3y = df_procesado.loc[df_procesado.index >= fecha_inicio].copy()
    
    # Redondear tasa de interés
    df_3y["Tasa_Interes"] = df_3y["Tasa_Interes"].round(2)
    
    # Crear columnas de año y mes
    df_3y.loc[:, "Año"] = df_3y.index.year
    df_3y.loc[:, "Mes"] = df_3y.index.month.astype(str)
    
    # Formatear mes con dos dígitos
    df_3y.loc[:, "Mes"] = df_3y["Mes"].apply(lambda x: f"{int(x):02d}")
    
    # Crear columna Año-Mes
    df_3y.loc[:, "Año-Mes"] = df_3y["Año"].astype(str) + "-" + df_3y["Mes"]
    
    # Reorganizar columnas finales
    df_final = df_3y[["Año-Mes", "Tasa_Interes"]].reset_index(drop=True)
    
    return df_final

def obtener_datos_desempleo(api_key: str, serie: str) -> pd.DataFrame:
    """Descarga y procesa los datos de la tasa de desempleo desde FRED."""
    try:
        fred = Fred(api_key=api_key)
        data = fred.get_series(serie)
        if data is None:
            raise ValueError(f"No se pudieron obtener datos para la serie: {serie}")
        
        df = pd.DataFrame(data, columns=["Tasa_Desempleo"])
        df.index = pd.to_datetime(df.index)
        return df
    except Exception as e:
        print(f"❌ Error al conectar o obtener datos de FRED: {e}")
        return None

def procesar_desempleo(df: pd.DataFrame) -> pd.DataFrame:
    """Procesa los datos de la tasa de desempleo."""
    df_procesado = df.copy()
    
    # Filtrar últimos 3 años
    fecha_inicio = df_procesado.index.max() - pd.DateOffset(years=3)
    df_3y = df_procesado.loc[df_procesado.index >= fecha_inicio].copy()
    
    # Redondear tasa de desempleo
    df_3y["Tasa_Desempleo"] = df_3y["Tasa_Desempleo"].round(2)
    
    # Crear columnas de año y mes
    df_3y.loc[:, "Año"] = df_3y.index.year
    df_3y.loc[:, "Mes"] = df_3y.index.month.astype(str)
    
    # Formatear mes con dos dígitos
    df_3y.loc[:, "Mes"] = df_3y["Mes"].apply(lambda x: f"{int(x):02d}")
    
    # Crear columna Año-Mes
    df_3y.loc[:, "Año-Mes"] = df_3y["Año"].astype(str) + "-" + df_3y["Mes"]
    
    # Reorganizar columnas finales
    df_final = df_3y[["Año-Mes", "Tasa_Desempleo"]].reset_index(drop=True)
    
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

    # Procesar inflación
    df_inflacion = obtener_datos_inflacion(api_key, Config.SERIE_INFLACION)
    if df_inflacion is not None:
        df_final_inflacion = calcular_inflacion(df_inflacion)
        print("--- Inflación (Últimos 12 meses) ---")
        print(df_final_inflacion.tail(12))
        print("---")
        guardar_a_excel(df_final_inflacion, Config.NOMBRE_ARCHIVO_INFLACION)

    # Procesar PIB
    df_pib = obtener_datos_pib(api_key, Config.SERIE_PIB)
    if df_pib is not None:
        df_final_pib = calcular_pib(df_pib)
        print("--- PIB (Últimos 12 trimestres) ---")
        print(df_final_pib.tail(12))
        print("---")
        guardar_a_excel(df_final_pib, Config.NOMBRE_ARCHIVO_PIB)

    # Procesar tasas de interés
    df_tasa_interes = obtener_datos_tasa_interes(api_key, Config.SERIE_TASA_INTERES)
    if df_tasa_interes is not None:
        df_final_tasa_interes = procesar_tasa_interes(df_tasa_interes)
        print("--- Tasas de Interés (Últimos 12 meses) ---")
        print(df_final_tasa_interes.tail(12))
        print("---")
        guardar_a_excel(df_final_tasa_interes, Config.NOMBRE_ARCHIVO_TASA_INTERES)

    # Procesar desempleo
    df_desempleo = obtener_datos_desempleo(api_key, Config.SERIE_DESEMPLEO)
    if df_desempleo is not None:
        df_final_desempleo = procesar_desempleo(df_desempleo)
        print("--- Tasa de Desempleo (Últimos 12 meses) ---")
        print(df_final_desempleo.tail(12))
        print("---")
        guardar_a_excel(df_final_desempleo, Config.NOMBRE_ARCHIVO_DESEMPLEO)

if __name__ == "__main__":
    main()