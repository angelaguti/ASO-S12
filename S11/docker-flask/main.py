from datetime import datetime
from app import create_app


app = create_app()

@app.route('/')
def hello():
    return {'message': 'Hola Luisito jeje me aburro mucho desde Flask en Docker!'}

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.route('/fecha')
def fecha():
    return {
            "fecha":
            datetime.now().isoformat(),
            "fecha_legible":
            datetime.now().strftime("%a %d %b %Y, %I:%M%p"),
           }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
