import os.path
import time
import pickle
import base64
from email.message import EmailMessage

from google import genai
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 🔐 SCOPES (permite leer y responder)
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# 🤖 GEMINI CONFIG (API NUEVA)
client = genai.Client(api_key="AIzaSyDTDwIK77ZSpsEFF2Eko5fKJ1WFDkK__54")  # <-- TU API KEY

# =========================
# UTILIDADES
# =========================

def obtener_headers(msg_data):
    headers = msg_data['payload']['headers']
    subject = sender = ""

    for h in headers:
        if h['name'] == 'Subject':
            subject = h['value']
        if h['name'] == 'From':
            sender = h['value']

    return sender, subject


def es_saludo(texto):
    saludos = [
        "hola",
        "buenos días",
        "buenas tardes",
        "buenas noches",
        "hey",
        "qué tal"
    ]
    texto = texto.lower()
    return any(s in texto for s in saludos)


def respuesta_gemini(texto):
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

    # 1️⃣ Token guardado
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # 2️⃣ Autenticación
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

    service = build('gmail', 'v1', credentials=creds)

    print("📬 Últimos 5 correos:\n")

    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=5
    ).execute()

    messages = results.get('messages', [])
    if not messages:
        print("No hay correos.")
        return

    ultimo_id_visto = messages[0]['id']

    for msg in messages:
        msg_data = service.users().messages().get(
            userId='me', id=msg['id'], format='full'
        ).execute()

        sender, subject = obtener_headers(msg_data)

        print("📧 Correo")
        print("De:", sender)
        print("Asunto:", subject)
        print("-" * 40)

    print("\n🤖 Agente activo. Esperando correos...\n")

    # =========================
    # LOOP PRINCIPAL
    # =========================
    while True:
        try:
            results = service.users().messages().list(
                userId='me', labelIds=['INBOX'], maxResults=1
            ).execute()

            messages = results.get('messages', [])

            if messages:
                msg_id = messages[0]['id']

                if msg_id != ultimo_id_visto:
                    ultimo_id_visto = msg_id

                    msg_data = service.users().messages().get(
                        userId='me', id=msg_id, format='full'
                    ).execute()

                    sender, subject = obtener_headers(msg_data)

                    print("📩 NUEVO CORREO")
                    print("De:", sender)
                    print("Asunto:", subject)

                    # 🎯 CONDICIÓN: solo Outlook + saludo
                    if (
                        sender and
                        "giovanni.20032026@outlook.com" in sender.lower() and
                        es_saludo(subject)
                    ):
                        respuesta = respuesta_gemini(subject)
                        responder_correo(service, sender, subject, respuesta)
                        print("🤖 Respuesta automática enviada")

                    print("-" * 40)

            time.sleep(10)

        except KeyboardInterrupt:
            print("\n🛑 Agente detenido por el usuario.")
            break


if __name__ == '__main__':
    main()
