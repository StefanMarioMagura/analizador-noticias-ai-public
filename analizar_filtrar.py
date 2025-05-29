from transformers import pipeline
import json

# Configuración
device = -1  # CPU, cambiar a 0 si tienes GPU disponible y configurada
modelo_sentimiento_nombre = "nlptown/bert-base-multilingual-uncased-sentiment"
modelo_fake_news_nombre = "mrm8488/bert-tiny-finetuned-fake-news-detection"
modelo_tematica_nombre = "facebook/bart-large-mnli"
modelo_emocional_nombre = "j-hartmann/emotion-english-distilroberta-base" # Recuerda: optimizado para inglés
modelo_resumen_nombre = "facebook/bart-large-cnn"

# Carga los modelos (asume que hiciste huggingface-cli login si fuera necesario para algún modelo)
# Es buena práctica manejar excepciones aquí si la carga de modelos falla (ej. por falta de conexión)
try:
    print("Cargando modelos de IA...")
    modelo_sentimiento = pipeline(
        "text-classification",
        model=modelo_sentimiento_nombre,
        device=device
    )

    modelo_fake_news = pipeline(
        "text-classification",
        model=modelo_fake_news_nombre,
        device=device
    )

    modelo_tematica = pipeline(
        "zero-shot-classification",
        model=modelo_tematica_nombre,
        device=device
    )

    modelo_emocional = pipeline(
        "text-classification",
        model=modelo_emocional_nombre,
        device=device,
        top_k=None  # Para obtener scores de todas las emociones
    )

    modelo_resumen = pipeline(
        "summarization",
        model=modelo_resumen_nombre,
        device=device
    )
    print("✅ Modelos cargados correctamente.")
except Exception as e:
    print(f"🚨 Error cargando los modelos: {e}")
    print("Asegúrate de tener conexión a internet y las librerías de Hugging Face instaladas correctamente.")
    exit() # Salir si los modelos no pueden cargarse


def analizar_sentimiento(texto):
    """Analiza el sentimiento del texto."""
    try:
        resultado = modelo_sentimiento(texto)[0]
        return resultado
    except Exception as e:
        print(f"Error en análisis de sentimiento: {e}")
        return {"label": "N/A", "score": 0.0}


def analizar_fake_news(texto):
    """Analiza si el texto es probable fake news."""
    try:
        resultado = modelo_fake_news(texto)[0]
        return resultado
    except Exception as e:
        print(f"Error en análisis de fake news: {e}")
        return {"label": "N/A", "score": 0.0}


def analizar_tematica(texto):
    """Clasifica el texto en una temática usando zero-shot."""
    posibles_categorias = ["salud", "tecnología", "educación", "deportes", "economía", "entretenimiento", "política", "ciencia", "medio ambiente", "cultura"] # Puedes ajustar esta lista
    try:
        resultado = modelo_tematica(texto, posibles_categorias, multi_label=False) # Asumimos una sola etiqueta principal
        etiqueta_principal = resultado["labels"][0]
        score_principal = resultado["scores"][0]
        return etiqueta_principal, score_principal
    except Exception as e:
        print(f"Error en análisis temático: {e}")
        return "N/A", 0.0


def analizar_emocional(texto):
    """Analiza la emoción predominante en el texto."""
    try:
        # El modelo devuelve una lista de listas de diccionarios si top_k=None
        # Si el texto es muy corto, podría no devolver lo esperado.
        resultados_emociones = modelo_emocional(texto)
        
        if resultados_emociones and isinstance(resultados_emociones, list) and resultados_emociones[0]:
            # Si top_k=None, devuelve una lista (para batch) que contiene otra lista de diccionarios
            # Para un solo texto, tomamos el primer elemento de la lista exterior
            lista_emociones = resultados_emociones[0]
            
            # Ordenamos para sacar la emoción con mayor score
            resultados_ordenados = sorted(lista_emociones, key=lambda x: x['score'], reverse=True)
            emocion_principal = resultados_ordenados[0]['label']
            score_emocion = resultados_ordenados[0]['score']
            return emocion_principal, score_emocion, resultados_ordenados # Devolvemos todos los detalles
        else:
            # Fallback si la estructura no es la esperada
            print(f"Respuesta inesperada del modelo emocional: {resultados_emociones}")
            return "N/A", 0.0, []

    except Exception as e:
        print(f"Error en análisis emocional: {e}")
        return "N/A", 0.0, []


def resumir_texto(texto, max_length=150, min_length=40): # Ajusta max/min length según tus necesidades
    """Genera un resumen del texto."""
    try:
        # Asegurarse de que el texto no sea demasiado corto para resumir, algunos modelos tienen límites.
        if len(texto.split()) < min_length / 2 : # Heurística muy simple
             return texto # Si es muy corto, devuelve el original o un mensaje

        resumen = modelo_resumen(texto, max_length=max_length, min_length=min_length, do_sample=False)
        texto_resumido = resumen[0]['summary_text']
        return texto_resumido
    except Exception as e:
        print(f"Error en resumen de texto: {e}")
        return "Resumen no disponible."


def cargar_noticias(ruta_archivo="noticias.json"):
    """Carga las noticias desde un archivo JSON."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            noticias = json.load(f)
        print(f"📰 Se han cargado {len(noticias)} noticias desde '{ruta_archivo}'.")
        return noticias
    except FileNotFoundError:
        print(f"🚨 Error: El archivo '{ruta_archivo}' no fue encontrado. Ejecuta primero 'main.py'.")
        return []
    except json.JSONDecodeError:
        print(f"🚨 Error: El archivo '{ruta_archivo}' contiene JSON inválido.")
        return []
    except Exception as e:
        print(f"🚨 Error inesperado al cargar noticias: {e}")
        return []


def determinar_categoria(estrellas, etiqueta_fake_news_label):
    """Determina una categoría final basada en estrellas de sentimiento y etiqueta de fake news."""
    # Convertimos la etiqueta del modelo de fake news a algo más legible
    # Asumimos que el modelo mrm8488... usa LABEL_0 para FAKE y LABEL_1 para REAL
    # ¡Verifica esto en la documentación del modelo si cambias de modelo!
    if etiqueta_fake_news_label == "LABEL_0": # FAKE
        fake_status = "FAKE"
    elif etiqueta_fake_news_label == "LABEL_1": # REAL
        fake_status = "REAL"
    else: # Si la etiqueta es N/A u otra cosa
        fake_status = "INDETERMINADO"

    umbral_estrellas_buena = 4 # A partir de 4 estrellas se considera sentimiento positivo para "Buena"

    if fake_status == "FAKE":
        return "Dudosa/Falsa"
    elif fake_status == "REAL":
        if estrellas >= umbral_estrellas_buena:
            return "Buena/Objetiva" # "Objetiva" aquí es por el sentimiento, no por un análisis de objetividad profundo
        else: # Menos de 4 estrellas pero real
            return "Subjetiva pero verdadera"
    else: # Si el fake_status es INDETERMINADO
        return "Veracidad no determinada"


def main():
    noticias_originales = cargar_noticias()
    if not noticias_originales:
        print("No hay noticias para procesar. Saliendo.")
        return

    print(f"\n🌀 Analizando {len(noticias_originales)} noticias...\n")

    noticias_destacadas_filtradas = []
    mejores_noticias_filtradas = []
    peores_noticias_filtradas = []
    # Puedes añadir más listas si necesitas otras categorizaciones directas aquí

    for i, noticia_original_data in enumerate(noticias_originales, 1):
        print(f"--- Procesando noticia {i}/{len(noticias_originales)}: {noticia_original_data.get('title', 'Sin título')} ---")

        # El texto para análisis se suele formar del título y la descripción
        texto_noticia = noticia_original_data.get("title", "") + ". " + noticia_original_data.get("description", "")
        if not texto_noticia.strip() or texto_noticia == ". ":
            print("Texto de noticia vacío o inválido, omitiendo.")
            continue

        # --- Realizar todos los análisis ---
        analisis_sentimiento = analizar_sentimiento(texto_noticia)
        label_sentimiento = analisis_sentimiento["label"]
        score_sentimiento = analisis_sentimiento["score"]
        
        # Extraer número de estrellas del sentimiento
        try:
            estrellas_sentimiento = int(label_sentimiento[0]) if label_sentimiento != "N/A" else 0
        except (ValueError, TypeError, IndexError):
            estrellas_sentimiento = 0 # Fallback si la etiqueta no es como "X stars"

        # Condición para omitir si la confianza del sentimiento es muy baja
        umbral_confianza_sentimiento = 0.3 # Ajusta este umbral si es necesario
        if score_sentimiento < umbral_confianza_sentimiento and label_sentimiento != "N/A":
            print(f"Sentimiento: {label_sentimiento} (confianza muy baja {score_sentimiento:.2f}), análisis poco fiable.")
            print("Se omite clasificación final basada en sentimiento por baja confianza.\n")
            # Podrías decidir continuar y marcarla como "Análisis no concluyente" en lugar de 'continue'
            # Por ahora, la saltamos para las listas principales, pero podrías guardarla en otra lista.
            # continue # Descomenta si quieres saltar completamente estas noticias

        analisis_fake = analizar_fake_news(texto_noticia)
        etiqueta_fake = analisis_fake["label"]
        score_fake = analisis_fake["score"]

        tema_principal, score_tema = analizar_tematica(texto_noticia)
        emocion_predominante, score_emocion, detalles_completos_emocion = analizar_emocional(texto_noticia)
        resumen_generado = resumir_texto(texto_noticia)

        # --- Determinar categoría final ---
        categoria_final_calculada = determinar_categoria(estrellas_sentimiento, etiqueta_fake)

        # --- Recopilar información de la fuente y URL ---
        fuente_data = noticia_original_data.get("source", {}) # GNews devuelve 'source' como un dict
        nombre_fuente = fuente_data.get("name", "Fuente Desconocida")
        url_articulo_original = noticia_original_data.get("url", "")
        url_imagen_articulo = noticia_original_data.get("image", "") # GNews usa 'image' para la URL de la imagen

        # --- Imprimir resultados para esta noticia ---
        print(f"Título: {noticia_original_data.get('title', 'Sin título')}")
        print(f"Sentimiento: {label_sentimiento} (Confianza: {score_sentimiento:.2f}, Estrellas: {estrellas_sentimiento})")
        print(f"Fake News: {etiqueta_fake} (Confianza: {score_fake:.2f})")
        print(f"Categoría Final IA: {categoria_final_calculada}")
        print(f"Tema Principal: {tema_principal} (Confianza: {score_tema:.2f})")
        print(f"Emoción Predominante: {emocion_predominante} (Confianza: {score_emocion:.2f})")
        print(f"Resumen: {resumen_generado}\n")

        # --- Crear el diccionario con toda la información para guardar ---
        noticia_procesada_completa = {
            "titulo": noticia_original_data.get("title"),
            "descripcion_original": noticia_original_data.get("description"), # Guardamos la original
            "url_noticia": url_articulo_original,
            "imagen_url": url_imagen_articulo,
            "fuente_nombre": nombre_fuente,
            "sentimiento": label_sentimiento,
            "confianza_sentimiento": score_sentimiento,
            "estrellas_sentimiento": estrellas_sentimiento, # Útil tener las estrellas directamente
            "fake_news": etiqueta_fake, # Etiqueta original del modelo (LABEL_0 o LABEL_1)
            "confianza_fake": score_fake,
            "categoria_final": categoria_final_calculada,
            "tema": tema_principal,
            "confianza_tema": score_tema,
            "emocion": emocion_predominante,
            "confianza_emocion": score_emocion,
            "detalles_emocion": detalles_completos_emocion, # Lista completa de emociones y scores
            "resumen": resumen_generado
        }

        # --- Clasificación en las listas principales para noticias_filtradas.json ---
        # (Puedes ajustar esta lógica según tus necesidades)
        # Noticias destacadas: Buenas/Objetivas Y emoción neutra/calma/contenta
        emociones_neutras_positivas = ["neutral", "calm", "content"] # Ajusta si tu modelo usa otras etiquetas
        if categoria_final_calculada == "Buena/Objetiva" and emocion_predominante.lower() in emociones_neutras_positivas:
            noticias_destacadas_filtradas.append(noticia_procesada_completa)
        
        # Mejores noticias: Buenas/Objetivas Y con alto rating de estrellas (y no necesariamente emoción neutra)
        # Usamos 'elif' para que no se dupliquen si ya están en 'destacadas' por la emoción.
        # Si quieres que puedan estar en ambas, quita el 'elif' y usa 'if'.
        elif categoria_final_calculada == "Buena/Objetiva" and estrellas_sentimiento >= 4:
            mejores_noticias_filtradas.append(noticia_procesada_completa)
        
        # Peores noticias: Dudosas/Falsas O con muy bajo rating de estrellas (aunque sean verdaderas)
        elif categoria_final_calculada == "Dudosa/Falsa" or (etiqueta_fake == "LABEL_1" and estrellas_sentimiento <= 2):
            peores_noticias_filtradas.append(noticia_procesada_completa)
        
        # Aquí podrías añadir más 'elif' o 'if' para otras categorías que quieras pre-filtrar en el JSON.

    # --- Guardar resultado en archivo para la web ---
    resultado_final_para_json = {
        "noticias_destacadas": noticias_destacadas_filtradas,
        "mejores_noticias": mejores_noticias_filtradas,
        "peores_noticias": peores_noticias_filtradas
        # Puedes añadir más claves aquí si creaste más listas.
    }

    ruta_salida_filtradas = "noticias_filtradas.json"
    try:
        with open(ruta_salida_filtradas, "w", encoding="utf-8") as f:
            json.dump(resultado_final_para_json, f, ensure_ascii=False, indent=4) # indent=4 para mejor lectura
        print(f"✅ Análisis completado. Resultados guardados en '{ruta_salida_filtradas}'")
    except Exception as e:
        print(f"🚨 Error al guardar {ruta_salida_filtradas}: {e}")

    # --- Llamada a la función para extraer noticias 100% objetivas (según criterios más estrictos) ---
    # Esta función ahora usará el mismo `noticia_procesada_completa` que tiene todos los campos.
    extraer_noticias_totalmente_objetivas(todas_las_noticias_procesadas_completas=noticias_originales, #Pasa las originales para referencia
                                         noticias_ya_analizadas=resultado_final_para_json)


def extraer_noticias_totalmente_objetivas(todas_las_noticias_procesadas_completas, noticias_ya_analizadas):
    """
    Extrae noticias consideradas "totalmente objetivas" de todas las noticias analizadas.
    Esta función es un ejemplo, podrías querer integrar su lógica de forma diferente
    o basarte en un conjunto más amplio que solo las listas de `noticias_ya_analizadas`.

    Por simplicidad, vamos a iterar sobre TODAS las noticias que se procesaron
    (podrías reconstruir esta lista a partir de `noticias_ya_analizadas` o, mejor aún,
    guardar una lista de *todas* las `noticia_procesada_completa` en `main` y pasarla aquí).

    Vamos a simplificar: asumimos que `noticias_ya_analizadas` contiene todas las noticias que
    pasaron el filtro de confianza de sentimiento y queremos aplicar un filtro adicional sobre ellas.
    """
    
    noticias_objetivas_extraidas = []
    
    # Juntamos todas las noticias de las diferentes listas de `noticias_ya_analizadas`
    # para asegurar que consideramos todas las que fueron analizadas y categorizadas.
    # Esto podría tener duplicados si una noticia cae en múltiples categorías iniciales,
    # así que hay que tener cuidado o asegurar que las listas originales no se solapen demasiado.
    # Una forma más limpia sería tener una lista 'todas_las_analizadas' generada en main().
    
    # Para este ejemplo, vamos a iterar sobre las noticias que están en 'mejores_noticias' y 'destacadas'
    # ya que son las que probablemente cumplan más criterios de objetividad.
    candidatas_para_objetivas = noticias_ya_analizadas.get("noticias_destacadas", []) + \
                               noticias_ya_analizadas.get("mejores_noticias", [])
    
    # Eliminamos duplicados por si una noticia estuviera en ambas listas (basado en URL o título)
    vistas_urls = set()
    candidatas_unicas = []
    for noticia in candidatas_para_objetivas:
        if noticia.get("url_noticia") not in vistas_urls:
            candidatas_unicas.append(noticia)
            vistas_urls.add(noticia.get("url_noticia"))
        elif noticia.get("titulo") not in vistas_urls: # Fallback si no hay URL
             candidatas_unicas.append(noticia)
             vistas_urls.add(noticia.get("titulo"))


    for noticia_analizada in candidatas_unicas:
        # Condiciones para ser "totalmente objetiva":
        es_real = noticia_analizada.get("fake_news") == "LABEL_1"
        es_buena_objetiva_categoria = noticia_analizada.get("categoria_final") == "Buena/Objetiva"
        
        # Sentimiento neutro (3 estrellas) o ligeramente positivo pero no extremo
        # El modelo nlptown da estrellas. "3 stars" es el más neutro.
        sentimiento_noticia = noticia_analizada.get("sentimiento", "")
        es_sentimiento_neutro = sentimiento_noticia == "3 stars"
        
        # Emoción neutra
        emocion_noticia = noticia_analizada.get("emocion", "").lower()
        es_emocion_neutra = emocion_noticia in ["neutral", "calm"] # Ajusta según tu modelo

        # Podrías añadir un umbral de confianza para el tema si es relevante para la objetividad
        # confianza_tema = noticia_analizada.get("confianza_tema", 0)
        # tema_confiable = confianza_tema > 0.6 # Ejemplo

        if es_real and es_buena_objetiva_categoria and es_sentimiento_neutro and es_emocion_neutra:
            noticias_objetivas_extraidas.append(noticia_analizada)

    ruta_salida_objetivas = "noticias_objetivas.json"
    if noticias_objetivas_extraidas:
        try:
            with open(ruta_salida_objetivas, "w", encoding="utf-8") as f:
                json.dump(noticias_objetivas_extraidas, f, ensure_ascii=False, indent=4)
            print(f"✅ Se han guardado {len(noticias_objetivas_extraidas)} noticias totalmente objetivas en '{ruta_salida_objetivas}'")
        except Exception as e:
            print(f"🚨 Error al guardar {ruta_salida_objetivas}: {e}")
    else:
        mensaje_no_objetivas = {
            "mensaje": "🕊️ Hoy no se ha encontrado ninguna noticia que cumpla todos los criterios de 'totalmente objetiva'. Seguimos filtrando para ti."
        }
        try:
            with open(ruta_salida_objetivas, "w", encoding="utf-8") as f:
                json.dump(mensaje_no_objetivas, f, ensure_ascii=False, indent=4)
            print(f"🕊️ No se encontraron noticias totalmente objetivas. Mensaje guardado en '{ruta_salida_objetivas}'.")
        except Exception as e:
            print(f"🚨 Error al guardar mensaje en {ruta_salida_objetivas}: {e}")


if __name__ == "__main__":
    main()
    # La llamada a `extraer_noticias_totalmente_objetivas` ahora está dentro de `main`
    # para asegurar que se ejecuta después de que `resultado_final_para_json` esté listo.
    # O, si prefieres, la puedes llamar después de main() como antes,
    # pero necesitaría cargar 'noticias_filtradas.json' ella misma.
    # La he modificado para que reciba los datos procesados directamente.












