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


def procesar_correos(data):
    """
    data llega desde Google Apps Script con esta forma:
    {
      "from": "...",
      "subject": "...",
      "body": "..."
    }
    """

    remitente = data.get("from", "")
    asunto = data.get("subject", "")
    cuerpo = data.get("body", "")

    texto = f"{asunto}\n{cuerpo}"

    # Clasificación
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

    # Envío por SendGrid
    responder_correo(
        destinatario=remitente,
        asunto="Re: " + asunto,
        contenido=respuesta
    )

    # Log para el frontend
    return [{
        "tipo": tipo,
        "destinatario": remitente,
        "asunto": "Re: " + asunto,
        "contenido": respuesta
    }]
