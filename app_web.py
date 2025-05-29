import json
import streamlit as st

# Traducciones de emociones (puedes expandir esto)
emociones_traducidas = {
    "neutral": "Neutral",
    "calm": "Calma",
    "content": "Contento/a",
    "anger": "Enojo",
    "disgust": "Asco",
    "joy": "Alegría",
    "sadness": "Tristeza",
    "fear": "Miedo",
    # Añade más si tu modelo de emoción devuelve otras etiquetas
}

def cargar_datos(ruta="noticias_filtradas.json"):
    """Carga los datos de noticias filtradas desde un archivo JSON."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        # El JSON tiene claves como "noticias_destacadas", "mejores_noticias", etc.
        # Devolvemos el diccionario completo para que la app web pueda acceder a las secciones
        return datos
    except FileNotFoundError:
        st.error(f"Error: El archivo {ruta} no fue encontrado. Asegúrate de ejecutar primero el script de análisis.")
        return {} # Devuelve un diccionario vacío para evitar más errores
    except json.JSONDecodeError:
        st.error(f"Error: El archivo {ruta} contiene JSON inválido.")
        return {}
    except Exception as e:
        st.error(f"Error inesperado al cargar noticias: {e}")
        return {}

def formatear_fake_news(label_fake_news):
    """Formatea la etiqueta de fake news para mostrarla de forma amigable."""
    if label_fake_news == "LABEL_1": # Asumiendo que LABEL_1 es REAL
        return "✅ Verdadera"
    elif label_fake_news == "LABEL_0": # Asumiendo que LABEL_0 es FAKE
        return "❌ Falsa"
    return "⚠️ Desconocido"

def traducir_emocion(emocion_ingles):
    """Traduce la etiqueta de emoción al español si está en el diccionario."""
    return emociones_traducidas.get(emocion_ingles.lower(), emocion_ingles.capitalize())

def mostrar_noticia_card(noticia, index):
    """Muestra una noticia individual en formato de tarjeta."""
    st.markdown("---") # Separador visual

    # Usar columnas para imagen a la izquierda y texto a la derecha
    col1, col2 = st.columns([1, 3]) # Proporción de las columnas

    with col1:
        if noticia.get("imagen_url"):
            st.image(noticia["imagen_url"], use_container_width=True)
        else:
            st.caption("Sin imagen disponible") # Placeholder si no hay imagen

    with col2:
        # Título como un enlace a la noticia original, si la URL está disponible
        if noticia.get("url_noticia"):
            st.markdown(f"### [{noticia.get('titulo', 'Sin título')}]({noticia.get('url_noticia')})")
        else:
            st.markdown(f"### {noticia.get('titulo', 'Sin título')}")

        st.caption(f"Fuente: {noticia.get('fuente_nombre', 'N/A')}") # Necesitarías añadir 'fuente_nombre' a noticias_filtradas.json
                                                                    # o extraerlo del campo 'descripcion' si está ahí.
                                                                    # GNews lo da en source.name en el JSON original.

        st.markdown(f"_{noticia.get('resumen', 'Sin resumen disponible.')}_")

        # Detalles del análisis
        sentimiento_str = noticia.get('sentimiento', 'N/A')
        conf_sentimiento = noticia.get('confianza_sentimiento', 0) * 100
        st.markdown(f"**Sentimiento:** {sentimiento_str} ({conf_sentimiento:.0f}% conf.)")

        fake_news_label = noticia.get("fake_news", "N/A")
        conf_fake = noticia.get('confianza_fake', 0) * 100
        st.markdown(f"**Veracidad:** {formatear_fake_news(fake_news_label)} ({conf_fake:.0f}% conf.)")

        st.markdown(f"**Categoría IA:** {noticia.get('categoria_final', 'N/A')}")

        tema = noticia.get('tema', 'N/A')
        conf_tema = noticia.get('confianza_tema', 0) * 100
        if tema != 'N/A' and conf_tema > 30: # Solo muestra el tema si la confianza es > 30% (ajustable)
            st.markdown(f"**Tema principal:** {tema.capitalize()} ({conf_tema:.0f}% conf.)")
        else:
            st.markdown(f"**Tema principal:** No determinado con suficiente confianza")


        emocion_val = traducir_emocion(noticia.get("emocion", "N/A"))
        conf_emocion = noticia.get('confianza_emocion', 0) * 100
        st.markdown(f"**Emoción predominante:** {emocion_val} ({conf_emocion:.0f}% conf.)")

        # Podrías añadir un expander para más detalles si es necesario
        # with st.expander("Ver todos los scores de emoción"):
        #     st.json(noticia.get("detalles_emocion", {}))


def mostrar_seccion_noticias(titulo_seccion, lista_noticias):
    """Muestra una sección completa de noticias."""
    st.header(titulo_seccion)
    if lista_noticias:
        # st.write(f"Encontradas: {len(lista_noticias)} noticias") # Opcional: contador
        for i, noticia in enumerate(lista_noticias):
            mostrar_noticia_card(noticia, i)
    else:
        st.info("🕊️ No hay noticias para mostrar en esta sección en este momento.")
    st.markdown("---")


def app():
    st.set_page_config(page_title="NotiAnalyst AI", layout="wide", page_icon="📢")

    st.title("📢 NotiAnalyst AI - Análisis y Filtrado Inteligente")
    st.markdown("""
    *Bienvenido a NotiAnalyst AI, tu fuente de noticias analizadas con inteligencia artificial.
    Explora las noticias clasificadas por sentimiento, veracidad, tema y emoción.*
    """)

    # Cargar los datos estructurados
    datos_noticias = cargar_datos() # Carga el JSON con las diferentes secciones

    if not datos_noticias:
        st.warning("No se pudieron cargar los datos de las noticias. Por favor, ejecuta el script de análisis (`analizar_filtrar.py`) primero.")
        return

    # Definir las secciones que quieres mostrar y qué datos usar
    # Estas claves deben coincidir con las que usaste en `analizar_filtrar.py` al guardar `resultado_final`
    # y con las que se usan en `extraer_noticias_objetivas.py` (si decides integrar ese archivo)
    
    # Para las noticias objetivas, cargamos el archivo 'noticias_objetivas.json'
    try:
        with open("noticias_objetivas.json", "r", encoding="utf-8") as f:
            contenido_objetivas = json.load(f)
            if isinstance(contenido_objetivas, dict) and "mensaje" in contenido_objetivas:
                noticias_totalmente_objetivas = [] # Si es un mensaje, no hay noticias
            else:
                noticias_totalmente_objetivas = contenido_objetivas # Asume que es una lista de noticias
    except Exception: #FileNotFoundError, json.JSONDecodeError
        noticias_totalmente_objetivas = []


    # Ejemplo de secciones (ajusta según las claves de tu JSON 'noticias_filtradas.json')
    # y cómo las quieres presentar.
    # Tu 'noticias_filtradas.json' tiene: "noticias_destacadas", "mejores_noticias", "peores_noticias"

    # Sección de "Noticias 100% Objetivas" (del archivo noticias_objetivas.json)
    mostrar_seccion_noticias("🎯 Noticias Verificadas como Objetivas", noticias_totalmente_objetivas)

    # Sección "Destacadas" (Buenas y Objetivas con emoción neutra)
    mostrar_seccion_noticias("🌟 Noticias Destacadas (Buenas, Objetivas y Neutras)", datos_noticias.get("noticias_destacadas", []))

    # Sección "Mejores Noticias" (Buenas y Objetivas con >= 4 estrellas)
    # Para evitar duplicados con "Destacadas", podrías filtrarlas si hay solapamiento.
    # Por ahora, las mostramos tal cual vienen del JSON.
    mostrar_seccion_noticias("👍 Mejores Noticias (Buenas y Objetivas, rating alto)", datos_noticias.get("mejores_noticias", []))

    # Creamos listas para otras categorías basadas en todas las noticias procesadas
    # si no están directamente en 'noticias_filtradas.json' de la forma que quieres
    todas_las_noticias_procesadas = []
    for key in datos_noticias:
        todas_las_noticias_procesadas.extend(datos_noticias[key])
    
    # Eliminar duplicados si una noticia puede estar en múltiples listas originales de `datos_noticias`
    # Esto se puede hacer guardando los títulos o URLs ya mostrados y saltándolos.
    # O, mejor, hacer que las listas en `noticias_filtradas.json` sean exclusivas si es el objetivo.

    noticias_subjetivas_verdaderas = [
        n for n in todas_las_noticias_procesadas
        if n.get("fake_news") == "LABEL_1" and n.get("categoria_final") == "Subjetiva pero verdadera"
    ]
    mostrar_seccion_noticias("🧐 Noticias Subjetivas pero Verdaderas", noticias_subjetivas_verdaderas)


    noticias_dudosas_o_falsas = [
        n for n in todas_las_noticias_procesadas
        if n.get("categoria_final") == "Dudosa/Falsa" or n.get("fake_news") == "LABEL_0"
    ]
    mostrar_seccion_noticias("🚨 Noticias Dudosas o Posiblemente Falsas", noticias_dudosas_o_falsas)
    
    # Ejemplo de sección por emoción (puedes crear más o hacer esto dinámico con un selector)
    emocion_a_filtrar = "anger" # Puedes cambiar esto o hacerlo un input del usuario
    noticias_con_emocion_especifica = [
        n for n in todas_las_noticias_procesadas
        if n.get("emocion", "").lower() == emocion_a_filtrar and n.get("fake_news") == "LABEL_1" # Solo verdaderas con esa emocion
    ]
    mostrar_seccion_noticias(f"😠 Noticias (Verdaderas) con Emoción de {traducir_emocion(emocion_a_filtrar)}", noticias_con_emocion_especifica)

    st.sidebar.info("Proyecto de IA para análisis de noticias. Creado con Streamlit y Transformers.")
    # Podrías añadir filtros en la sidebar:
    # st.sidebar.multiselect("Filtrar por Tema:", ["salud", "tecnología", ...])


if __name__ == "__main__":
    app()


