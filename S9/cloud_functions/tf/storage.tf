# Bucket para almacenar código fuente durante build
resource "google_storage_bucket" "function_source" {
  name          = "${var.project_id}-function-source"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
}

# Subir código fuente al bucket
resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${filesha256("${path.module}/../main.py")}.zip"
  bucket = google_storage_bucket.function_source.name
  source = "${path.module}/../function-source.zip"
}
