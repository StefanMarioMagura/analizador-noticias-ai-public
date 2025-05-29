# NotiAnalyst AI 📢: Analizador Inteligente de Noticias

NotiAnalyst AI es una aplicación Python que utiliza Inteligencia Artificial para obtener, analizar, filtrar y presentar noticias. Realiza análisis de sentimiento, detección de noticias falsas, clasificación temática, análisis emocional y resumen de texto para ofrecer una perspectiva más profunda sobre la información.

## ✨ Características

* **Recopilación de Noticias**: Obtiene las últimas noticias en español utilizando la API de GNews.
* **Análisis Multifacético con IA**:
    * **Sentimiento**: Clasifica las noticias de 1 a 5 estrellas (modelo multilingüe).
    * **Detección de Fake News**: Identifica si una noticia es probablemente real o falsa.
    * **Clasificación Temática**: Determina el tema principal de la noticia (ej. deportes, tecnología) usando zero-shot classification.
    * **Análisis Emocional**: Detecta la emoción predominante en el texto (ej. alegría, enojo).
    * **Resumen Automático**: Genera un resumen conciso de cada noticia.
* **Categorización Personalizada**: Clasifica las noticias en categorías como "Buena/Objetiva", "Subjetiva pero verdadera", "Dudosa/Falsa".
* **Extracción de Noticias Objetivas**: Filtra y presenta un conjunto de noticias consideradas altamente objetivas según criterios estrictos.
* **Interfaz Web Interactiva**: Muestra las noticias analizadas en una aplicación web fácil de usar construida con Streamlit, con imágenes, resúmenes y todos los insights de la IA.

## 📂 Estructura del Proyecto

```
.
├── main.py                 # Script para obtener noticias de GNews API y guardarlas en noticias.json
├── analizar_filtrar.py     # Script principal para analizar noticias con IA y generar noticias_filtradas.json y noticias_objetivas.json
├── app_web.py              # Aplicación web Streamlit para visualizar las noticias analizadas
├── noticias.json           # (Generado) Noticias crudas obtenidas de GNews
├── noticias_filtradas.json # (Generado) Noticias analizadas y categorizadas para la web
├── noticias_objetivas.json # (Generado) Subconjunto de noticias altamente objetivas
├── .env                    # (Necesitas crearlo) Para guardar tu API Key de GNews
├── requirements.txt        # Dependencias de Python
└── README.md               # Este archivo
```
*(Opcional: `analizador_objetividad.py` - Script experimental para un análisis de objetividad alternativo, no integrado en el flujo principal de la app web.)*

## ⚙️ Requisitos Previos

* Python 3.8+
* pip (gestor de paquetes de Python)
* Una cuenta de Hugging Face (y haber iniciado sesión con `huggingface-cli login` si usas modelos que lo requieran, aunque los modelos actuales son públicos).
* Una API Key de [GNews.io](https://gnews.io/)

## 🚀 Instalación

1.  **Clona el repositorio (si está en uno) o descarga los archivos.**
    ```bash
    # Ejemplo si estuviera en Git
    # git clone [https://tu-repositorio-url.git](https://tu-repositorio-url.git)
    # cd tu-proyecto
    ```

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *Nota sobre PyTorch (`torch`)*: Si tienes problemas con la instalación de `torch` o quieres usar una versión específica para GPU, visita la [página oficial de PyTorch](https://pytorch.org/get-started/locally/) para obtener el comando de instalación adecuado para tu sistema y configuración de CUDA.

4.  **Configura tu API Key de GNews:**
    * Crea un archivo llamado `.env` en la raíz del proyecto.
    * Añade tu API Key de GNews al archivo `.env` de la siguiente manera:
        ```
        GNEWS_API_KEY=TU_API_KEY_AQUI
        ```

5.  **(Opcional) Login en Hugging Face CLI:**
    Si vas a usar modelos privados o algunos que requieran autenticación (los actuales no deberían, pero es buena práctica si expandes):
    ```bash
    huggingface-cli login
    ```
    Esto guardará tu token de Hugging Face localmente.

## ▶️ Uso

El proceso se divide en tres pasos principales:

1.  **Obtener Noticias Crudas:**
    Ejecuta `main.py` para descargar las últimas noticias de GNews. Esto creará o actualizará el archivo `noticias.json`.
    ```bash
    python main.py
    ```
    Puedes cambiar el número de noticias a descargar editando el parámetro `max` en `main.py`.

2.  **Analizar y Filtrar Noticias con IA:**
    Ejecuta `analizar_filtrar.py` para procesar las noticias de `noticias.json`. Este script aplicará todos los modelos de IA y generará:
    * `noticias_filtradas.json`: Contiene las noticias analizadas y organizadas en secciones como "destacadas", "mejores", "peores".
    * `noticias_objetivas.json`: Contiene un subconjunto de noticias consideradas altamente objetivas.
    ```bash
    python analizar_filtrar.py
    ```
    Este proceso puede tardar un poco dependiendo del número de noticias y la potencia de tu CPU/GPU.

3.  **Visualizar en la Aplicación Web:**
    Lanza la aplicación Streamlit para ver e interactuar con las noticias analizadas.
    ```bash
    streamlit run app_web.py
    ```
    Abre tu navegador web y ve a la dirección URL local que te indica Streamlit (usualmente `http://localhost:8501`).

Para mantener la aplicación actualizada, deberás ejecutar los pasos 1 y 2 periódicamente.

## 🔧 Solución de Posibles Errores

* **`GNEWS_API_KEY` no encontrada / Error de API**:
    * Asegúrate de que el archivo `.env` existe en la raíz del proyecto y contiene `GNEWS_API_KEY=TU_API_KEY_REAL`.
    * Verifica que tu API Key de GNews sea válida y no haya excedido la cuota.
* **Errores al descargar modelos de Hugging Face**:
    * Comprueba tu conexión a internet.
    * Asegúrate de tener suficiente espacio en disco (los modelos pueden ser grandes).
    * Algunos modelos pueden ser eliminados o movidos; verifica el nombre del modelo en [Hugging Face Model Hub](https://huggingface.co/models).
* **Problemas de dependencias (`ModuleNotFoundError`)**:
    * Asegúrate de haber activado tu entorno virtual.
    * Ejecuta `pip install -r requirements.txt` nuevamente.
* **Rendimiento Lento del Análisis**:
    * El análisis de IA, especialmente con múltiples modelos, puede ser intensivo.
    * Si tienes una GPU compatible con CUDA y PyTorch configurado para GPU (cambiando `device = 0` en `analizar_filtrar.py`), el proceso será más rápido.
    * Reduce el número de noticias a analizar si es necesario para pruebas.
* **Modelo Emocional en Español**:
    * El modelo `j-hartmann/emotion-english-distilroberta-base` está entrenado en inglés. Para noticias en español, su precisión puede variar. Considera buscar modelos de análisis de emociones multilingües o específicos para español en Hugging Face si los resultados no son satisfactorios.
* **Resultados de "Tema Principal" no satisfactorios**:
    * El análisis temático zero-shot depende de la calidad del texto y de la lista de `posibles_categorias` definida en `analizar_filtrar.py`. Puedes ajustar estas categorías.
    * La interfaz web ahora muestra el tema solo si la confianza es superior a un umbral (30% por defecto en `app_web.py`, puedes ajustarlo).

## 퓨 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el proyecto, por favor abre un issue o un pull request (si estuviera en un repositorio público).