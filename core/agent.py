import pickle
import os
import os

EN_VERCEL = os.environ.get("VERCEL") == "1"

from core.gmail_auth import obtener_servicio_gmail
from core.gmail_reader import obtener_headers_y_cuerpo
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

RESPONDIDOS_FILE = "respondidos.pkl"
EMAIL_PERMITIDO = "giovanni.20032026@outlook.com"


    

def procesar_correos():
    service = obtener_servicio_gmail()
    logs = []

    if EN_VERCEL:
            return [{
                "tipo": "Info",
                "destinatario": "",
                "asunto": "",
                "contenido": "Ejecución en Vercel: Gmail deshabilitado temporalmente."
            }]
    
    if os.path.exists(RESPONDIDOS_FILE):
        with open(RESPONDIDOS_FILE, 'rb') as f:
            correos_respondidos = pickle.load(f)
    else:
        correos_respondidos = set()

    results = service.users().messages().list(
        userId='me',
        q="is:unread",
        maxResults=5
    ).execute()

    messages = results.get('messages', [])

    if not messages:
        logs.append({
            "tipo": "Info",
            "destinatario": "",
            "asunto": "",
            "contenido": "No hay correos nuevos."
        })
        return logs

    for msg in messages:
        msg_id = msg['id']

        if msg_id in correos_respondidos:
            continue

        msg_data = service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        sender, subject, body = obtener_headers_y_cuerpo(msg_data)

        # 🔒 FILTRO DE REMITENTE
        if EMAIL_PERMITIDO not in sender.lower():
            logs.append({
                "tipo": "Ignorado",
                "destinatario": sender,
                "asunto": subject,
                "contenido": "Remitente no permitido."
            })
            continue

        texto = f"{subject}\n{body}"

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
            logs.append({
                "tipo": "Ignorado",
                "destinatario": sender,
                "asunto": subject,
                "contenido": "El correo no coincide con ninguna categoría."
            })
            continue

        responder_correo(service, sender, subject, respuesta)

        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

        correos_respondidos.add(msg_id)

        # 📤 LOG ESTRUCTURADO PARA EL FRONTEND
        logs.append({
            "tipo": tipo,
            "destinatario": sender,
            "asunto": "Re: " + subject,
            "contenido": respuesta
        })

    with open(RESPONDIDOS_FILE, 'wb') as f:
        pickle.dump(correos_respondidos, f)

    return logs
