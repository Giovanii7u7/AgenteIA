import os
from google import genai

# 🔐 Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# 🤖 Gemini (Vercel-safe)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("DEBUG GEMINI_API_KEY:", GEMINI_API_KEY)

if not GEMINI_API_KEY:
    # ⚠️ No crasheamos la app completa en import
    print("⚠️ GEMINI_API_KEY no definida (entorno actual)")
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)



# 📅 Fechas oficiales (valor por defecto)
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
