# IAM binding para permitir invocaciones públicas (solo para pruebas)
resource "google_cloudfunctions2_function_iam_member" "public_invoker" {
  project        = var.project_id
  location       = var.region
  cloud_function = google_cloudfunctions2_function.hello_http_terraform.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}
