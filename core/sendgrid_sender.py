import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

FROM_EMAIL = "giovaniarango6@gmail.com"

def responder_correo(destinatario, asunto, contenido):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=destinatario,
        subject=asunto,
        plain_text_content=contenido
    )

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    sg.send(message)
