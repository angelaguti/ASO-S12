import json
import functions_framework
from flask import Request

@functions_framework.http
def hello_http(request: Request):
    # Obtener parámetros de la query string
    sum1 = request.args.get('sum1')
    sum2 = request.args.get('sum2')

    # Validación: parámetros obligatorios
    if sum1 is None or sum2 is None:
        return (
            json.dumps({"error": "Debes proporcionar sum1 y sum2 en la query string"}),
            400,
            {'Content-Type': 'application/json'}
        )

    # Convertir a enteros y sumar
    try:
        result = int(sum1) + int(sum2)
    except ValueError:
        return (
            json.dumps({"error": "sum1 y sum2 deben ser números enteros"}),
            400,
            {'Content-Type': 'application/json'}
        )

    # Construir respuesta
    response_data = {
        "sum1": sum1,
        "sum2": sum2,
        "resultado": result
    }

    return json.dumps(response_data), 200, {'Content-Type': 'application/json'}
