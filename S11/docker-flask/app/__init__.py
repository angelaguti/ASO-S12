"""
Aplicación Flask con SQLAlchemy y PostgreSQL
Este archivo configura Flask-SQLAlchemy y crea la aplicación
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

# Crear instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    """
    Factory function que crea y configura la aplicación Flask.
    Este patrón permite crear múltiples instancias de la app para testing.
    """
    app = Flask(__name__)
    
    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Construir cadena de conexión a PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.environ.get('DB_USER')}:"
        f"{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:"
        f"{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME')}"
    )
    
    print("Cadena de conexión: ", app.config['SQLALCHEMY_DATABASE_URI'])
    #generara una cadena tal que 
    #postgresql://user:supersecreto@db:5432/taskdatabase

    # Desactivar tracking de modificaciones (ahorra recursos)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar SQLAlchemy con la aplicación
    db.init_app(app)
    
    # Importar modelos (debe hacerse después de crear db)
    from app.models import Task
    
    # Importar y registrar blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    # Crear tablas en la base de datos (solo si no existen)
    with app.app_context():
        db.create_all()
    
    return app
