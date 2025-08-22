import requests
import pandas as pd

# Configuración
cik_apple = "0000320193"  # CIK de Apple
headers = {"User-Agent": "email@gmail.com"}  # SEC exige identificarse

# Función para obtener un concepto financiero desde la API XBRL de la SEC
def get_concept(cik, concept):
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
    r = requests.get(url, headers=headers)
    data = r.json()

    # Verificar qué unidades existen
    if "units" not in data:
        print(f"⚠️ {concept}: no tiene datos en la respuesta")
        return pd.DataFrame()

    # Buscar si tiene USD
    if "USD" in data["units"]:
        df = pd.DataFrame(data["units"]["USD"])
        return df
    else:
        print(f"⚠️ {concept}: no tiene valores en USD. Claves disponibles: {list(data['units'].keys())}")
        return pd.DataFrame()

# Conceptos clave
concepts = {
    "Revenues": "Revenues",
    "NetIncome": "NetIncomeLoss",
    "EPS": "EarningsPerShareBasic",
    "Assets": "Assets",
    "Liabilities": "Liabilities",
    "Equity": "StockholdersEquity"
}

# Descargar cada métrica y quedarnos con los últimos 12 meses (~4 trimestres)
dfs = {}
for name, concept in concepts.items():
    df_concept = get_concept(cik_apple, concept)
    if not df_concept.empty:
        df_concept = df_concept.sort_values("end", ascending=False).head(4)
        df_concept = df_concept[["end", "val"]].rename(columns={"val": name})
        dfs[name] = df_concept.reset_index(drop=True)

# Combinar todo en un único DataFrame
df_final = dfs["Revenues"]
for name in ["NetIncome", "EPS", "Assets", "Liabilities", "Equity"]:
    if name in dfs:  # solo combinar si existe
        df_final[name] = dfs[name][name]

# Calcular ratios si los datos existen
if "NetIncome" in df_final and "Equity" in df_final:
    df_final["ROE"] = (df_final["NetIncome"] / df_final["Equity"]).round(2)
if "Liabilities" in df_final and "Assets" in df_final:
    df_final["DebtRatio"] = (df_final["Liabilities"] / df_final["Assets"]).round(2)

# Redondear valores numéricos
for col in df_final.columns[1:]:
    df_final[col] = df_final[col].round(2)

# Guardar en Excel
nombre_archivo = "apple_financials.xlsx"
df_final.to_excel(nombre_archivo, index=False, engine="openpyxl")

print(f"✅ Archivo guardado como {nombre_archivo}")
print(df_final)
