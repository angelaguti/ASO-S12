import json
import csv
import functions_framework
from datetime import datetime
from google.cloud import storage

@functions_framework.cloud_event
def process_csv_file(cloud_event):
    """
    Cloud Run function que procesa archivos CSV al subirse a Cloud Storage.
    
    El decorator @functions_framework.cloud_event indica que esta función
    manejará eventos en formato CloudEvents estándar.
    
    Args:
        cloud_event: Objeto CloudEvent con el evento recibido
    """
    # Los datos del evento están en cloud_event.data (atributo del objeto CloudEvent)
    # cloud_event es un objeto CloudEvent, no un diccionario, por lo que usamos el atributo .data
    event_data = cloud_event.data if cloud_event.data else {}
    
    # Extraer información del evento de Storage
    file_name = event_data.get('name')
    bucket_name = event_data.get('bucket')
    
    # Acceder a metadata del evento usando subscript (el objeto CloudEvent soporta acceso como diccionario)
    event_type = cloud_event['type']
    
    print(f"Evento recibido: {event_type}")
    print(f"Procesando archivo: {file_name} del bucket: {bucket_name}")
    
    # Inicializar cliente de Storage
    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(file_name)
    
    # Leer contenido del archivo
    file_content = source_blob.download_as_text()
    
    # Procesar CSV
    csv_reader = csv.DictReader(file_content.splitlines())
    
    # Calcular estadísticas
    total_rows = 0
    column_names = []
    sample_data = []
    
    for row in csv_reader:
        if not column_names:
            column_names = list(row.keys())
        
        total_rows += 1
        if total_rows <= 3:  # Guardar primeras 3 filas como muestra
            sample_data.append(row)
    
    # Crear resumen
    summary = {
        'file_name': file_name,
        'bucket_name': bucket_name,
        'total_rows': total_rows,
        'columns': column_names,
        'sample_data': sample_data[:3],
        'processed_at': datetime.utcnow().isoformat(),
        'event_id': cloud_event['id'],
        'event_time': cloud_event['time']
    }
    
    # Escribir resumen a bucket de salida
    output_bucket_name = f"{bucket_name}-processed"
    output_bucket = storage_client.bucket(output_bucket_name)
    output_blob_name = f"summary_{file_name}.json"
    output_blob = output_bucket.blob(output_blob_name)
    
    output_blob.upload_from_string(
        json.dumps(summary, indent=2),
        content_type='application/json'
    )
    
    print(f"Resumen guardado en: gs://{output_bucket_name}/{output_blob_name}")
    
    # Retornar indicador de éxito
    return "OK"

