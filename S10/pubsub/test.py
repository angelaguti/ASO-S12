import requests
import json
from datetime import datetime

# Obtener PROJECT_ID
project_id = "angela-aso-git"

# Simular evento PubSub
cloud_event = {
  "subscription": "projects/my-project/subscriptions/my-subscription",
  "message": {
    "@type": "type.googleapis.com/google.pubsub.v1.PubsubMessage",
    "attributes": {
      "attr1":"attr1-value"
    },
    "data": "dGVzdCBtZXNzYWdlIDM=",
    "messageId": "message-id",
    "publishTime":"2021-02-05T04:06:14.109Z"
  }
}

print("Enviando evento CloudEvent a función local...")

# Enviar evento a la función local
response = requests.post(
    'http://localhost:8080',
    json=cloud_event,
    headers={'Content-Type': 'application/json'}
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.text}")
