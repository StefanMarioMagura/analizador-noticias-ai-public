
# 🚀 NotiAnalyst AI: Tu Analizador Inteligente de Noticias

---

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub last commit](https://img.shields.io/github/last-commit/StefanMarioMagura/analizador-noticias-ai-public?style=flat)](https://github.com/StefanMarioMagura/analizador-noticias-ai-public/commits/main)

NotiAnalyst AI es una potente aplicación en Python diseñada para **obtener, analizar, filtrar y presentar noticias** de forma inteligente utilizando técnicas avanzadas de Inteligencia Artificial. Desde el análisis de sentimiento hasta la detección de noticias falsas y el resumen automático, esta herramienta ofrece una perspectiva profunda y multifacética sobre la información actual, presentada en una interfaz web interactiva con Streamlit.

---

## ✨ Características Destacadas

* **Recopilación Inteligente**: Obtiene las últimas noticias en español a través de la API de GNews.
* **Análisis Multifacético con IA**:
    * **Análisis de Sentimiento**: Clasifica el tono de cada noticia en una escala de 1 a 5 estrellas, utilizando un modelo BERT multilingüe.
    * **Detección de "Fake News"**: Identifica la probabilidad de que una noticia sea real o falsa, contribuyendo a un consumo de información más crítico.
    * **Clasificación Temática**: Determina el tema principal de la noticia (e.g., deportes, tecnología, política) mediante **clasificación zero-shot**, sin necesidad de entrenamiento previo.
    * **Análisis Emocional**: Detecta la emoción predominante en el texto (e.g., alegría, enojo, tristeza), ofreciendo una capa adicional de entendimiento.
    * **Resumen Automático**: Genera resúmenes concisos y coherentes de cada noticia, facilitando la comprensión rápida.
* **Categorización Personalizada**: Clasifica las noticias según su objetividad y veracidad percibida: "Buena/Objetiva", "Subjetiva pero verdadera", y "Dudosa/Falsa".
* **Extracción de Noticias Objetivas**: Filtra y presenta un subconjunto de noticias consideradas de alta objetividad, basadas en criterios de análisis rigurosos.
* **Interfaz Web Interactiva**: Visualiza todos los análisis y datos en una aplicación web intuitiva desarrollada con **Streamlit**, que incluye imágenes, resúmenes y todos los insights de la IA.

---
## 📂 Estructura del Proyecto

La organización principal de tu proyecto es la siguiente:

-   `main.py`                     # Script principal: obtiene noticias de GNews API -> noticias.json
-   `analizar_filtrar.py`         # Módulo de IA: procesa datos -> noticias_filtradas.json, noticias_objetivas.json
-   `app_web.py`                  # Aplicación web Streamlit para visualización interactiva
-   `noticias.json`               # (Generado) Almacena las noticias crudas de GNews
-   `noticias_filtradas.json`     # (Generado y Necesario para app web) Noticias con análisis de IA
-   `noticias_objetivas.json`     # (Generado y Necesario para app web) Noticias filtradas por objetividad
-   `requirements.txt`            # Lista de dependencias de Python

-   `README.md`                   # Este archivo


---

## ⚙️ Requisitos Previos

Para ejecutar NotiAnalyst AI localmente, asegúrate de tener instalado lo siguiente:

* **Python 3.8+**
* **pip** (gestor de paquetes de Python)
* **Git**
* Una cuenta de [GitHub](https://github.com/) (para clonar el repositorio).
* Una **API Key de [GNews.io](https://gnews.io/)**. (Necesaria para `main.py`).

---

## 🚀 Instalación y Uso Local

Sigue estos pasos para poner en marcha NotiAnalyst AI en tu máquina local:

1.  **Clona el Repositorio:**
    Abre tu terminal y clona este proyecto.
    ```bash
    git clone [https://github.com/StefanMarioMagura/analizador-noticias-ai-public.git](https://github.com/StefanMarioMagura/analizador-noticias-ai-public.git) # Reemplaza con la URL de tu nuevo repo
    cd analizador-noticias-ai-public # Reemplaza con el nombre de tu repo
    ```

2.  **Configura tu Entorno Virtual (altamente recomendado):**
    Crear un entorno virtual aísla las dependencias de tu proyecto.
    ```bash
    python -m venv venv
    # Para activar en Windows:
    venv\Scripts\activate
    # Para activar en macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instala las Dependencias:**
    Todas las librerías necesarias están listadas en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    * **Nota sobre PyTorch (`torch`):** Si encuentras problemas con la instalación de `torch` o deseas aprovechar tu GPU, visita la [página oficial de PyTorch](https://pytorch.org/get-started/locally/) para obtener el comando de instalación específico para tu sistema.

4.  **Configura tu API Key de GNews:**
    Dado que esta es una versión pública del proyecto, la API Key no está incluida en el código por seguridad.

    * **Opción A: Inyectar la clave directamente en el código (solo si el repositorio es privado, con extrema precaución):**
        Si tu repositorio es **privado**, puedes añadir tu clave directamente en `main.py` donde se usa `API_KEY`.
        ```python
        # Ejemplo en main.py (NO HACER SI EL REPOSITORIO ES PÚBLICO)
        API_KEY = "TU_CLAVE_REAL_DE_GNEWS_AQUI"
        ```
    * **Opción B: Usar una variable de entorno del sistema (recomendado para seguridad y flexibilidad):**
        Establece `API_KEY` como una variable de entorno en tu sistema operativo.
        * **En Windows:** Busca "Editar las variables de entorno del sistema" -> "Variables de entorno..." -> "Nueva..." en Variables de usuario, con `Nombre de la variable: API_KEY` y `Valor de la variable: tu_clave_de_gnews_aqui`. Cierra y reabre tu terminal.
        * Luego, en tu código Python, asegúrate de que se accede a la variable:
            ```python
            import os
            API_KEY = os.getenv("API_KEY")
            ```

---

## ▶️ Flujo de Uso (Ejecución Local)

NotiAnalyst AI opera en tres fases principales:

1.  **Obtener Noticias Crudas:**
    Descarga las últimas noticias de GNews. Esto creará o actualizará el archivo `noticias.json`.
    ```bash
    python main.py
    ```

2.  **Analizar y Filtrar Noticias con IA:**
    Procesa las noticias de `noticias.json` aplicando todos los modelos de IA. Esto generará o actualizará `noticias_filtradas.json` y `noticias_objetivas.json`. Este paso puede consumir recursos y tiempo, dependiendo del volumen de noticias y tu hardware.
    ```bash
    python analizar_filtrar.py
    ```

3.  **Visualizar en la Aplicación Web:**
    Inicia la interfaz interactiva de Streamlit para explorar los resultados del análisis.
    ```bash
    streamlit run app_web.py
    ```
    Una vez lanzada, abre tu navegador y visita la URL proporcionada por Streamlit (generalmente `http://localhost:8501`).

---

## 🌐 Despliegue (Ejemplo con Streamlit Community Cloud)

Puedes desplegar NotiAnalyst AI fácilmente para compartirla con el mundo:

1.  Asegúrate de que **tu proyecto esté en un repositorio de GitHub público**.
2.  **¡Importante!** Los archivos `noticias_filtradas.json` y `noticias_objetivas.json` deben estar **actualizados y subidos** a tu repositorio de GitHub. Estos JSON son los que la aplicación web leerá para mostrar los datos analizados.
3.  Visita [share.streamlit.io](https://share.streamlit.io/), conecta tu cuenta de GitHub, y despliega la aplicación seleccionando tu repositorio y el archivo `app_web.py`.

---

## 🔧 Solución de Posibles Errores Comunes

* **`API_KEY` no encontrada / Error de API**:
    * Verifica que has configurado correctamente tu `API_KEY` como variable de entorno del sistema o directamente en el código (si es privado).
    * Asegúrate de que tu API Key de GNews sea válida y que no hayas excedido tu cuota de solicitudes.
* **Errores al descargar modelos de Hugging Face (en `analizar_filtrar.py`)**:
    * Comprueba tu conexión a internet.
    * Asegúrate de tener suficiente espacio en disco en tu máquina.
* **`ModuleNotFoundError`**:
    * Confirma que tu entorno virtual está activo y que ejecutaste `pip install -r requirements.txt` correctamente.
* **Problemas de rendimiento durante el análisis**:
    * El procesamiento de IA es intensivo en recursos. Considera la posibilidad de utilizar una GPU (`device=0` en tu código, si tienes una y está configurada) para acelerar el proceso.
    * Para pruebas, puedes reducir el número de noticias que se obtienen en `main.py`.
