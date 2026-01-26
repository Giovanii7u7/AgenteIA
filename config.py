from google import genai

# 🔐 Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# 🤖 Gemini
client = genai.Client(api_key="AIzaSyDTDwIK77ZSpsEFF2Eko5fKJ1WFDkK__54")

# 📅 Fechas oficiales
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
