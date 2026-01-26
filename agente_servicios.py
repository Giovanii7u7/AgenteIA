import os.path
import time
import pickle
import base64
from email.message import EmailMessage

from google import genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 🔐 SCOPES (leer y responder correos)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# 🤖 GEMINI CONFIG
client = genai.Client(api_key="AIzaSyDTDwIK77ZSpsEFF2Eko5fKJ1WFDkK__54")
# =========================
# FECHAS OFICIALES
# =========================

FECHAS_ESCOLARES = """
📅 FECHAS IMPORTANTES – SERVICIOS ESCOLARES 2026

• Entrega de fichas:
  🗓️ 13 de febrero al 26 de junio de 2026

• Examen Diagnóstico:
  🗓️ 23 de mayo o 01 de julio de 2026

• Resultados del Examen Diagnóstico:
  🗓️ 06 de julio de 2026

• Inscripciones al curso propedéutico:
  🗓️ 13 al 24 de julio de 2026

• Curso propedéutico:
  🗓️ Del 27 de julio al 18 de septiembre de 2026

• Inscripción a 1er semestre:
  🗓️ Del 21 al 30 de septiembre de 2026

• Inicio de semestre:
  🗓️ Octubre de 2026
"""

# =========================
# UTILIDADES
# =========================

def obtener_headers_y_cuerpo(msg_data):
    headers = msg_data['payload']['headers']
    subject = sender = ""

    for h in headers:
        if h['name'] == 'Subject':
            subject = h['value']
        if h['name'] == 'From':
            sender = h['value']

    body = ""
    payload = msg_data['payload']

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    else:
        data = payload['body'].get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')

    return sender, subject, body


def es_saludo(texto):
    saludos = [
        "hola", "buenos días", "buenas tardes",
        "buenas noches", "hey", "qué tal"
    ]
    texto = texto.lower()
    return any(s in texto for s in saludos)


def es_consulta_fechas(texto):
    palabras_clave = [
        "fecha", "fechas", "reinscripción", "inscripción",
        "examen", "diagnóstico", "propedéutico",
        "semestre", "inicio", "resultados","reinscripciones","reinscribo"
    ]
    texto = texto.lower()
    return any(p in texto for p in palabras_clave)

# =========================
# RESPUESTAS IA
# =========================

def respuesta_saludo(texto):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Responde de forma amable, corta y natural.
El correo recibido es solo un saludo.

Correo:
"{texto}"
"""
    )
    return response.text


def respuesta_servicios_escolares():
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
Eres el área de Servicios Escolares de una institución educativa.
Responde de manera formal, clara y amable.

Incluye un saludo breve y presenta la siguiente información oficial:

{FECHAS_ESCOLARES}
"""
    )
    return response.text

# =========================
# RESPONDER CORREO
# =========================

def responder_correo(service, destinatario, asunto_original, respuesta_texto):
    mensaje = EmailMessage()
    mensaje.set_content(respuesta_texto)

    mensaje['To'] = destinatario
    mensaje['Subject'] = "Re: " + asunto_original

    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

    service.users().messages().send(
        userId='me',
        body={'raw': raw}
    ).execute()

# =========================
# MAIN
# =========================

def main():
    creds = None

    # Token OAuth
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_451085285960-4puqvo98933bt68kppap95lkq1avjj0k.apps.googleusercontent.com.json',
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Correos ya respondidos
    if os.path.exists('respondidos.pkl'):
        with open('respondidos.pkl', 'rb') as f:
            correos_respondidos = pickle.load(f)
    else:
        correos_respondidos = set()

    service = build('gmail', 'v1', credentials=creds)

    print("🤖 Agente activo. Esperando correos...\n")

    while True:
        try:
            results = service.users().messages().list(
                userId='me', labelIds=['INBOX'], maxResults=1
            ).execute()

            messages = results.get('messages', [])

            if messages:
                msg_id = messages[0]['id']

                if msg_id not in correos_respondidos:
                    msg_data = service.users().messages().get(
                        userId='me', id=msg_id, format='full'
                    ).execute()

                    sender, subject, body = obtener_headers_y_cuerpo(msg_data)

                    texto_total = f"{subject}\n{body}"

                    print("📩 NUEVO CORREO")
                    print("De:", sender)
                    print("Asunto:", subject)

                    if sender and "giovanni.20032026@outlook.com" in sender.lower():

                        if es_saludo(texto_total):
                            respuesta = respuesta_saludo(texto_total)
                            responder_correo(service, sender, subject, respuesta)
                            print("🤖 Respuesta de saludo enviada")

                        elif es_consulta_fechas(texto_total):
                            respuesta = respuesta_servicios_escolares()
                            responder_correo(service, sender, subject, respuesta)
                            print("🤖 Respuesta de servicios escolares enviada")

                        correos_respondidos.add(msg_id)
                        with open('respondidos.pkl', 'wb') as f:
                            pickle.dump(correos_respondidos, f)

                    print("-" * 40)

            time.sleep(10)

        except KeyboardInterrupt:
            print("\n🛑 Agente detenido por el usuario.")
            break


if __name__ == '__main__':
    main()