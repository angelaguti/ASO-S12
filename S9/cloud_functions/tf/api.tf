# Habilitar Cloud Functions API
resource "google_project_service" "cloudfunctions_api" {
  service = "cloudfunctions.googleapis.com"
  
  disable_on_destroy = false
}

# Habilitar Cloud Build API (requerido para deploy)
resource "google_project_service" "cloudbuild_api" {
  service = "cloudbuild.googleapis.com"
  
  disable_on_destroy = false
}
