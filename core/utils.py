def es_saludo(texto):
    saludos = [
        "hola", "buenos días", "buenas tardes",
        "buenas noches", "hey", "qué tal"
    ]
    texto = texto.lower()
    return any(s in texto for s in saludos)


def es_consulta_fechas(texto):
    palabras = [
        "fecha", "fechas", "reinscripción", "inscripción",
        "examen", "diagnóstico", "propedéutico",
        "semestre", "inicio", "resultados","reinscripciones","reinscribo"
    ]
    texto = texto.lower()
    return any(p in texto for p in palabras)


def es_consulta_costos_pagos(texto):
    palabras = [
        "costo", "costos", "pago", "pagos", "cuota", "cuotas",
        "colegiatura", "colegiaturas", "precio", "inscripción",
        "reinscripción", "mensualidad"
    ]
    texto = texto.lower()
    return any(p in texto for p in palabras)


def es_consulta_becas(texto):
    palabras = [
        "beca", "becas", "apoyo", "apoyos",
        "ayuda económica", "alimentaria",
        "jóvenes escribiendo el futuro",
        "telmex", "federal"
    ]
    texto = texto.lower()
    return any(p in texto for p in palabras)
