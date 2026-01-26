import base64

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
