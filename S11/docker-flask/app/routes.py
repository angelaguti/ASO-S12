"""
Rutas de la API Flask
Este archivo define todos los endpoints de la API REST para gestionar tareas
"""

from flask import Blueprint, request, jsonify
from app import db
from app.models import Task

# Crear Blueprint para las rutas
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Endpoint raíz que proporciona información sobre la API"""
    return {
        'message': 'Flask app with PostgreSQL',
        'endpoints': {
            'GET /tasks': 'Listar todas las tareas',
            'GET /tasks/<id>': 'Obtener una tarea específica',
            'POST /tasks': 'Crear una nueva tarea',
            'PUT /tasks/<id>': 'Actualizar una tarea',
            'DELETE /tasks/<id>': 'Eliminar una tarea',
            'GET /health': 'Health check'
        }
    }

@bp.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok'}

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Obtener todas las tareas.
    
    Returns:
        JSON: Lista de todas las tareas en formato JSON
    """
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Obtener una tarea específica por ID.
    
    Args:
        task_id: ID de la tarea a obtener
        
    Returns:
        JSON: Datos de la tarea o error 404 si no existe
    """
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Crear una nueva tarea.
    
    Body (JSON):
        - title: Título de la tarea (obligatorio)
        - description: Descripción de la tarea (opcional)
        - completed: Estado de completado (opcional, default: False)
        
    Returns:
        JSON: Datos de la tarea creada con código 201
    """
    data = request.get_json()
    
    # Validación básica
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Crear nueva tarea
    task = Task(
        title=data.get('title'),
        description=data.get('description', ''),
        completed=data.get('completed', False)
    )
    
    # Añadir a la sesión y guardar
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Actualizar una tarea existente.
    
    Args:
        task_id: ID de la tarea a actualizar
        
    Body (JSON):
        - title: Nuevo título (opcional)
        - description: Nueva descripción (opcional)
        - completed: Nuevo estado de completado (opcional)
        
    Returns:
        JSON: Datos de la tarea actualizada o error 404 si no existe
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    # Actualizar campos si están presentes en el request
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    
    # Guardar cambios
    db.session.commit()
    
    return jsonify(task.to_dict())

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """
    Eliminar una tarea.
    
    Args:
        task_id: ID de la tarea a eliminar
        
    Returns:
        Empty response con código 204 (No Content) o error 404 si no existe
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204




