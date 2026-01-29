import requests
from config import client
from core.data_store import cargar_info

# Puedes cambiar el modelo cuando quieras
# Opciones seguras y baratas:
# - mistralai/mistral-7b-instruct
# - openai/gpt-3.5-turbo
# - meta-llama/llama-3-8b-instruct
MODEL_NAME = "mistralai/mistral-7b-instruct"


def _generar_respuesta(prompt: str) -> str:
    """
    Genera una respuesta usando OpenRouter.
    Maneja errores sin romper la app.
    """
    if client is None:
        return "El servicio de IA no está disponible en este momento."

    try:
        response = requests.post(
            f"{client['base_url']}/chat/completions",
            headers={
                "Authorization": f"Bearer {client['api_key']}",
                "Content-Type": "application/json",
                # Header recomendado por OpenRouter
                "HTTP-Referer": "https://agente-ia.vercel.app",
                "X-Title": "Agente Servicios Escolares"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "Eres un asistente institucional de Servicios Escolares."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Error OpenRouter:", e)
        return "Ocurrió un problema al generar la respuesta. Intente más tarde."


def respuesta_saludo(texto):
    return _generar_respuesta(f"""
Responde de forma amable, corta y natural.
El correo recibido es solo un saludo.

Correo:
"{texto}"
""")


def respuesta_servicios_escolares():
    info = cargar_info()
    fechas = info.get(
        "fechas_escolares",
        "La información de fechas escolares no está disponible actualmente."
    )

    return _generar_respuesta(f"""
Responde de manera formal, clara y amable.

Incluye un saludo breve y presenta la siguiente información oficial:

{fechas}
""")


def respuesta_costos_pagos():
    info = cargar_info()
    costos = info.get(
        "costos",
        "La información sobre costos y pagos no está disponible actualmente."
    )

    return _generar_respuesta(f"""
Responde de manera formal, clara y amable.

Indica la siguiente información oficial:

{costos}

Finaliza ofreciendo apoyo en caso de dudas adicionales.
""")


def respuesta_becas():
    info = cargar_info()
    becas = info.get(
        "becas",
        "La información sobre becas no está disponible actualmente."
    )

    return _generar_respuesta(f"""
Responde de manera formal, clara y amable.

Incluye la siguiente información oficial sobre becas:

{becas}

Finaliza invitando a acudir a Servicios Escolares para orientación personalizada.
""")
