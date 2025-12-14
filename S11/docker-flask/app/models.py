"""
Modelos SQLAlchemy para la aplicación
Este archivo define los modelos de datos que representan las tablas en PostgreSQL
"""

from app import db
from datetime import datetime

class Task(db.Model):
    """
    Modelo que representa una tarea en la base de datos.
    
    Este modelo se mapea a una tabla 'tasks' en PostgreSQL con las siguientes columnas:
    - id: Identificador único (clave primaria)
    - title: Título de la tarea (obligatorio)
    - description: Descripción detallada (opcional)
    - completed: Estado de completado (False por defecto)
    - created_at: Fecha y hora de creación (automática)
    """
    __tablename__ = 'tasks'
    
    # Definición de columnas
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """
        Convierte el objeto Task a un diccionario.
        Útil para serializar a JSON en APIs REST.
        
        Returns:
            dict: Diccionario con todos los atributos de la tarea
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        """
        Representación en string del objeto.
        Útil para debugging y logging.
        
        Returns:
            str: Representación legible del objeto
        """
        return f'<Task {self.id}: {self.title}>'
