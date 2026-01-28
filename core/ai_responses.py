from config import client
from core.data_store import cargar_info

MODEL_NAME = "gemini-2.5-flash"


def _generar_respuesta(prompt: str) -> str:
    """
    Función centralizada para generar contenido con Gemini.
    Evita repetir lógica y maneja errores de forma segura.
    """
    if client is None:
        return "El servicio de IA no está disponible en este momento."

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


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
Eres el área de Servicios Escolares.
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
Eres el área de Servicios Escolares.
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
Eres el área de Servicios Escolares.
Responde de manera formal, clara y amable.

Incluye la siguiente información oficial sobre becas:

{becas}

Finaliza invitando a acudir a Servicios Escolares para orientación personalizada.
""")
