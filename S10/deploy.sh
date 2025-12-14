PROJECT_ID=$(gcloud config get project)
echo "Project id: $PROJECT_ID"

INPUT_BUCKET_NAME="gs://lab-storage-input-$PROJECT_ID"
OUTPUT_BUCKET_NAME="$INPUT_BUCKET_NAME-processed"
FUNCTION_NAME=test-gcs-event

echo "$INPUT_BUCKET_NAME ---output--> $OUTPUT_BUCKET_NAME"

if ! gsutil ls $INPUT_BUCKET_NAME
then
    echo "WARNING! El bucket $INPUT_BUCKET_NAME no existe"
    echo "Procedo a crearlo"
    gsutil mb $INPUT_BUCKET_NAME
else
    echo "OK! Bucket $INPUT_BUCKET_NAME existe"
fi

if ! gsutil ls $OUTPUT_BUCKET_NAME
then
    echo "WARNING! El bucket $OUTPUT_BUCKET_NAME no existe"
    echo "Procedo a crearlo"
    gsutil mb $
else
    echo "OK! Bucket $OUTPUT_BUCKET_NAME existe"
fi

gcloud functions deploy $FUNCTION_NAME \
  --gen2 \
  --runtime=python311 \
  --region=europe-west1 \
  --source=. \
  --entry-point=process_csv_file \
  --trigger-bucket=$INPUT_BUCKET_NAME \
  --memory=256MB \
  --timeout=300s \
  --set-env-vars="OUTPUT_BUCKET=$OUTPUT_BUCKET_NAME"
