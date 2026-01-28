import config
from core.sendgrid_sender import responder_correo
from core.utils import (
    es_saludo,
    es_consulta_fechas,
    es_consulta_costos_pagos,
    es_consulta_becas
)
from core.ai_responses import (
    respuesta_saludo,
    respuesta_servicios_escolares,
    respuesta_costos_pagos,
    respuesta_becas
)

EMAIL_PERMITIDO = "giovanni.20032026@outlook.com"

def procesar_correos(data):
    remitente = data.get("from", "").lower()
    asunto = data.get("subject", "")
    cuerpo = data.get("body", "")

    # 🔒 FILTRO DE REMITENTE
    if EMAIL_PERMITIDO not in remitente:
        return [{
            "tipo": "Ignorado",
            "destinatario": remitente,
            "asunto": asunto,
            "contenido": "Remitente no autorizado. No se respondió."
        }]

    texto = f"{asunto}\n{cuerpo}"

    if es_consulta_fechas(texto):
        respuesta = respuesta_servicios_escolares()
        tipo = "Fechas"

    elif es_consulta_costos_pagos(texto):
        respuesta = respuesta_costos_pagos()
        tipo = "Costos y pagos"

    elif es_consulta_becas(texto):
        respuesta = respuesta_becas()
        tipo = "Becas"

    elif es_saludo(texto):
        respuesta = respuesta_saludo(texto)
        tipo = "Saludo"

    else:
        respuesta = respuesta_saludo(texto)
        tipo = "General"

    # 📤 Envío por SendGrid (solo si pasó el filtro)
    responder_correo(
        destinatario=remitente,
        asunto="Re: " + asunto,
        contenido=respuesta
    )

    return [{
        "tipo": tipo,
        "destinatario": remitente,
        "asunto": "Re: " + asunto,
        "contenido": respuesta
    }]