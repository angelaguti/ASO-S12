"""
Archivo de configuración de Locust para pruebas de carga
Genera tareas con títulos y descripciones aleatorias usando Faker
"""

from locust import HttpUser, task, between
from faker import Faker
import json

class TaskUser(HttpUser):
    """
    Usuario simulado que interactúa con la API de tareas.
    Utiliza Faker para generar datos aleatorios de tareas.
    """
    wait_time = between(1, 3)  # Espera entre 1 y 3 segundos entre tareas
    
    def on_start(self):
        """Inicializa Faker al comenzar cada usuario simulado"""
        self.faker = Faker('es_ES')  # Usa español de España para datos más realistas
    
    @task(3)
    def create_task(self):
        """
        Crea una nueva tarea con título y descripción aleatorios.
        Peso 3: se ejecuta 3 veces más frecuentemente que otras tareas.
        """
        task_data = {
            "title": self.faker.sentence(nb_words=4),  # Genera un título de 4 palabras
            "description": self.faker.text(max_nb_chars=200),  # Descripción de hasta 200 caracteres
            "completed": self.faker.boolean(chance_of_getting_true=30)  # 30% de probabilidad de estar completada
        }
        
        with self.client.post(
            "/tasks",
            json=task_data,
            catch_response=True,
            name="POST /tasks"
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Expected 201, got {response.status_code}")
    
    @task(2)
    def list_tasks(self):
        """
        Lista todas las tareas disponibles.
        Peso 2: se ejecuta con frecuencia media.
        """
        with self.client.get(
            "/tasks",
            catch_response=True,
            name="GET /tasks"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Expected 200, got {response.status_code}")
    
    @task(1)
    def get_task(self):
        """
        Obtiene una tarea específica por ID.
        Primero lista las tareas para obtener IDs válidos.
        Peso 1: se ejecuta con menor frecuencia.
        """
        # Primero obtenemos la lista de tareas para tener IDs válidos
        response = self.client.get("/tasks", name="GET /tasks (for ID)")
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                # Seleccionamos un ID aleatorio de las tareas existentes
                import random
                task_id = random.choice(tasks)['id']
                
                with self.client.get(
                    f"/tasks/{task_id}",
                    catch_response=True,
                    name="GET /tasks/[id]"
                ) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Expected 200, got {response.status_code}")
    
    @task(1)
    def update_task(self):
        """
        Actualiza una tarea existente con nuevos datos aleatorios.
        Peso 1: se ejecuta con menor frecuencia.
        """
        # Primero obtenemos la lista de tareas
        response = self.client.get("/tasks", name="GET /tasks (for update)")
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                import random
                task_id = random.choice(tasks)['id']
                
                # Generamos nuevos datos aleatorios para la actualización
                update_data = {
                    "title": self.faker.sentence(nb_words=4),
                    "description": self.faker.text(max_nb_chars=200),
                    "completed": self.faker.boolean(chance_of_getting_true=50)
                }
                
                with self.client.put(
                    f"/tasks/{task_id}",
                    json=update_data,
                    catch_response=True,
                    name="PUT /tasks/[id]"
                ) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Expected 200, got {response.status_code}")
    
    @task(1)
    def delete_task(self):
        """
        Elimina una tarea existente.
        Peso 1: se ejecuta con menor frecuencia.
        """
        # Primero obtenemos la lista de tareas
        response = self.client.get("/tasks", name="GET /tasks (for delete)")
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                import random
                task_id = random.choice(tasks)['id']
                
                with self.client.delete(
                    f"/tasks/{task_id}",
                    catch_response=True,
                    name="DELETE /tasks/[id]"
                ) as response:
                    if response.status_code == 200:
                        response.success()
                    else:
                        response.failure(f"Expected 200, got {response.status_code}")
