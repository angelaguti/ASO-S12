from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    """Ejemplo básico de endpoint Flask"""
    # https://host.com/recurso/subrecurso?querystring
    # querystring -> atrib=valor&atrib2=valor2&atrib3=valor3&...
    # Obtener parámetro de query string
    name = request.args.get('name', 'Mundo')
    
    # Si es POST, intentar obtener del body JSON
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        name = data.get('name', name)
    
    return jsonify({
        'message': f'Hola, {name}!',
        'method': request.method
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
