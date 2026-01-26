from config import client
from core.data_store import cargar_info


def respuesta_saludo(texto):
    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Responde de forma amable, corta y natural.
El correo recibido es solo un saludo.

Correo:
"{texto}"
"""
    )
    return r.text


def respuesta_servicios_escolares():
    info = cargar_info()
    fechas = info.get(
        "fechas_escolares",
        "La información de fechas escolares no está disponible actualmente."
    )

    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Eres el área de Servicios Escolares de una institución educativa.
Responde de manera formal, clara y amable.

Incluye un saludo breve y presenta la siguiente información oficial:

{fechas}
"""
    )
    return r.text


def respuesta_costos_pagos():
    info = cargar_info()
    costos = info.get(
        "costos",
        "La información sobre costos y pagos no está disponible actualmente."
    )

    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Eres el área de Servicios Escolares de la Universidad del Istmo.
Responde de manera formal, clara y amable.

Indica la siguiente información oficial:

{costos}

Finaliza ofreciendo apoyo en caso de dudas adicionales.
"""
    )
    return r.text


def respuesta_becas():
    info = cargar_info()
    becas = info.get(
        "becas",
        "La información sobre becas no está disponible actualmente."
    )

    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Eres el área de Servicios Escolares de la Universidad del Istmo.
Responde de manera formal, clara y amable.

Incluye la siguiente información oficial sobre becas:

{becas}

Finaliza invitando a acudir a Servicios Escolares para orientación personalizada.
"""
    )
    return r.text
