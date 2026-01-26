import base64
from email.message import EmailMessage

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
