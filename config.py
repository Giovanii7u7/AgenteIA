import os
import google.generativeai as genai

# 🔐 Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# 🤖 Configuración de Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY no está definida en las variables de entorno")

genai.configure(api_key=GEMINI_API_KEY)

# 📅 Fechas oficiales (valor por defecto)
FECHAS_ESCOLARES = """
📅 FECHAS IMPORTANTES – SERVICIOS ESCOLARES 2026
...
"""
