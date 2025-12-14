import json
import functions_framework
from flask import Request

@functions_framework.http
def hello_http(request: Request):
    """
    Cloud Run function con HTTP trigger.
    
    El decorador @functions_framework.http indica que esta función
    manejará peticiones HTTP. Recibe un objeto flask.Request.
    
    Args:
        request: Objeto Request de Flask con la petición HTTP
    
    Returns:
        Tupla (response_body, status_code, headers) o
        string simple o
        objeto Response de Flask
    """
    # Obtener parámetros de query string
    name = request.args.get('name')
    
    # Obtener del body JSON si es POST/PUT
    if request.is_json:
        json_data = request.get_json()
        if json_data and 'name' in json_data:
            name = json_data['name']
    
    # Valor por defecto
    if not name:
        name = 'Mundo'
    
    # Construir respuesta
    response_data = {
        'message': f'Hola, que tal, {name}!',
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers)
    }
    
    # Retornar como tupla (body, status, headers)
    return json.dumps(response_data), 200, {'Content-Type': 'application/json'}

    # Alternativamente, puedes retornar solo el string:
    # return json.dumps(response_data)
    
    # O usar Flask Response:
    # from flask import jsonify
    # return jsonify(response_data)
