import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")

url = f"Usa tu clave de API de gnew para obtener noticias"

response = requests.get(url)
print("Código de estado:", response.status_code)

if response.status_code == 200:
    data = response.json()
    articles = data.get("articles", [])

    if articles:
        # Guardar en archivo JSON
        with open("noticias.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)
        print("✅ Noticias guardadas en 'noticias.json'\n")

        # Mostrar en consola
        for i, articulo in enumerate(articles, 1):
            print(f"\n📰 Noticia {i}")
            print(f"Título: {articulo['title']}")
            print(f"Descripción: {articulo['description']}")
            print(f"Fuente: {articulo['source']['name']}")
            print(f"URL: {articulo['url']}")
    else:
        print("No se encontraron noticias.")
else:
    print("Error:", response.status_code, response.text)



