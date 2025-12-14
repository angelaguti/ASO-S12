# Cloud Run Function (Gen 2)
resource "google_cloudfunctions2_function" "hello_http_terraform" {
  name        = "hello-http-terraform"
  location    = var.region
  description = "Cloud Run function desplegada con Terraform"
  
  build_config {
    runtime     = "python311"
    entry_point = "hello_http"
    source {
      storage_source {
        bucket = google_storage_bucket.function_source.name
        object = google_storage_bucket_object.function_source.name
      }
    }
  }
  
  service_config {
    max_instance_count = 10
    min_instance_count = 0
    available_memory  = "256M"
    timeout_seconds   = 60
    
    ingress_settings               = "ALLOW_ALL"
    all_traffic_on_latest_revision = true
    
    # Permitir invocaciones sin autenticación (solo para pruebas)
    environment_variables = {
      ENV = "development"
    }
  }
  
  depends_on = [
    google_project_service.cloudfunctions_api,
    google_project_service.cloudbuild_api
  ]
}
