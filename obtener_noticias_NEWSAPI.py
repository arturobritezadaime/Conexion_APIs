# Importa la clase Config en lugar de la variable
from config import Config
from newsapi import NewsApiClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


newsapi = NewsApiClient(api_key=Config.NEWSAPI_API_KEY)

def resumir_noticia(texto, max_palabras=150):
    """
    Función para resumir un texto.
    """
    if not texto or len(texto.split()) < 100:  # Evita resumir textos muy cortos
        return texto

    palabras_irrelevantes = set(stopwords.words('english'))
    palabras = word_tokenize(texto)

    # Contar la frecuencia de cada palabra
    frecuencia_palabras = {}
    for palabra in palabras:
        if palabra.lower() not in palabras_irrelevantes:
            if palabra.lower() not in frecuencia_palabras:
                frecuencia_palabras[palabra.lower()] = 1
            else:
                frecuencia_palabras[palabra.lower()] += 1

    # Normalizar las frecuencias
    max_frecuencia = max(frecuencia_palabras.values())
    for palabra in frecuencia_palabras:
        frecuencia_palabras[palabra] = (frecuencia_palabras[palabra] / max_frecuencia)

    # Calcular la puntuación de cada oración
    oraciones = sent_tokenize(texto)
    puntuacion_oraciones = {}
    for oracion in oraciones:
        for palabra in word_tokenize(oracion.lower()):
            if palabra in frecuencia_palabras:
                if oracion not in puntuacion_oraciones:
                    puntuacion_oraciones[oracion] = frecuencia_palabras[palabra]
                else:
                    puntuacion_oraciones[oracion] += frecuencia_palabras[palabra]

    # Construir el resumen
    resumen = ''
    palabras_en_resumen = 0
    for oracion in sorted(puntuacion_oraciones, key=puntuacion_oraciones.get, reverse=True):
        if palabras_en_resumen + len(oracion.split()) <= max_palabras:
            resumen += ' ' + oracion
            palabras_en_resumen += len(oracion.split())
        else:
            break

    return resumen.strip()

# Obtener las 5 noticias más recientes sobre Google
print("Obteniendo noticias y resúmenes para Google...\n")

try:
    articulos_google = newsapi.get_everything(
        q='Google', 
        language='en', 
        sort_by='publishedAt', 
        page_size=5
    )

    articulos = articulos_google.get('articles', [])

    if articulos:
        for i, articulo in enumerate(articulos):
            contenido = articulo.get('content', '')
            if contenido:
                print(f"--- Artículo [{i+1}] - Título: {articulo.get('title')} ---")
                resumen = resumir_noticia(contenido)
                print(f"Resumen: {resumen}\n")
            else:
                print(f"--- Artículo [{i+1}] - Título: {articulo.get('title')} ---")
                print("No se pudo obtener el contenido completo para resumir.\n")

    else:
        print("No se encontraron noticias recientes para Google.")

except Exception as e:
    print(f"Ocurrió un error: {e}")