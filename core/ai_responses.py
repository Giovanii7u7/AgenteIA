import google.generativeai as genai
from core.data_store import cargar_info

MODEL_NAME = "gemini-2.5-flash"


def _get_model():
    return genai.GenerativeModel(MODEL_NAME)


def respuesta_saludo(texto):
    model = _get_model()
    response = model.generate_content(f"""
Responde de forma amable, corta y natural.
El correo recibido es solo un saludo.

Correo:
"{texto}"
""")
    return response.text


def respuesta_servicios_escolares():
    info = cargar_info()
    fechas = info.get("fechas_escolares", "Información no disponible.")

    model = _get_model()
    response = model.generate_content(f"""
Eres el área de Servicios Escolares.
Responde de manera formal y clara.

{fechas}
""")
    return response.text


def respuesta_costos_pagos():
    info = cargar_info()
    costos = info.get("costos", "Información no disponible.")

    model = _get_model()
    response = model.generate_content(f"""
Eres el área de Servicios Escolares.
Indica la siguiente información oficial:

{costos}
""")
    return response.text


def respuesta_becas():
    info = cargar_info()
    becas = info.get("becas", "Información no disponible.")

    model = _get_model()
    response = model.generate_content(f"""
Eres el área de Servicios Escolares.
Incluye la siguiente información sobre becas:

{becas}
""")
    return response.text
