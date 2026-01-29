import requests
from config import OPENROUTER_API_KEY
from core.data_store import cargar_info

# 🔹 Modelo recomendado (barato y estable)
# Otras opciones válidas:
# - meta-llama/llama-3-8b-instruct
# - openai/gpt-3.5-turbo
MODEL_NAME = "mistralai/mistral-7b-instruct"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _generar_respuesta(prompt: str) -> str:
    """
    Genera una respuesta usando OpenRouter.
    Maneja errores sin romper la app (ideal para Vercel).
    """

    if not OPENROUTER_API_KEY:
        return "El servicio de IA no está disponible en este momento."

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                # Recomendado por OpenRouter
                "HTTP-Referer": "https://agente-ia-iota.vercel.app",
                "X-Title": "Agente Servicios Escolares"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente institucional del área de Servicios Escolares."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("❌ Error OpenRouter:", e)
        return "Ocurrió un problema al generar la respuesta. Intente más tarde."


# ===================== RESPUESTAS =====================

def respuesta_saludo(texto: str) -> str:
    return _generar_respuesta(f"""
Responde de forma amable, corta y natural.
El correo recibido es únicamente un saludo.

Correo:
"{texto}"
""")


def respuesta_servicios_escolares() -> str:
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


def respuesta_costos_pagos() -> str:
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


def respuesta_becas() -> str:
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
