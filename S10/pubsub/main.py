import base64
import functions_framework
import os
import uuid
import json
from google.cloud import storage

bucket_name = os.environ["BUCKET_NAME"]
blob_name = os.environ["BLOB_NAME"]

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    print(f"Mensaje recibido! -- [ {message} ]")

    # Inicializar cliente de Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name+str(uuid.uuid4()))

    summary = {
        "message": message,
        "is_color": message in ["azul", "rojo", "amarillo"],
        "is_city": message in ["madrid", "barcelona", "alicante"]
    }


    blob.upload_from_string(
        json.dumps(summary, indent=2),
        content_type='application/json'
    )

