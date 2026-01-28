import google.generativeai as genai
from core.data_store import cargar_info


# =====================================================
# 🤝 SALUDO
# =====================================================
def respuesta_saludo(texto):
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(f"""
Responde de forma amable, corta y natural.
El correo recibido es solo un saludo.

Correo:
"{texto}"
""")

    return response.text


# =====================================================
# 📅 FECHAS ESCOLARES
# =====================================================
def respuesta_servicios_escolares():
    info = cargar_info()
    fechas = info.get(
        "fechas_escolares",
        "La información de fechas escolares no está disponible actualmente."
    )

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(f"""
Eres el área de Servicios Escolares de una institución educativa.
Responde de manera formal, clara y amable.

Incluye un saludo breve y presenta la siguiente información oficial:

{fechas}
""")

    return response.text


# =====================================================
# 💰 COSTOS Y PAGOS
# =====================================================
def respuesta_costos_pagos():
    info = cargar_info()
    costos = info.get(
        "costos",
        "La información sobre costos y pagos no está disponible actualmente."
    )

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(f"""
Eres el área de Servicios Escolares de la Universidad del Istmo.
Responde de manera formal, clara y amable.

Indica la siguiente información oficial:

{costos}

Finaliza ofreciendo apoyo en caso de dudas adicionales.
""")

    return response.text


# =====================================================
# 🎓 BECAS
# =====================================================
def respuesta_becas():
    info = cargar_info()
    becas = info.get(
        "becas",
        "La información sobre becas no está disponible actualmente."
    )

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(f"""
Eres el área de Servicios Escolares de la Universidad del Istmo.
Responde de manera formal, clara y amable.

Incluye la siguiente información oficial sobre becas:

{becas}

Finaliza invitando a acudir a Servicios Escolares para orientación personalizada.
""")

    return response.text
