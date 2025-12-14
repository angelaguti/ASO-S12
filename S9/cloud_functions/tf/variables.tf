# Variable para project ID
variable "project_id" {
  description = "ID del proyecto GCP"
  type        = string
}

# Variable para región
variable "region" {
  description = "Región donde desplegar recursos"
  type        = string
  default     = "europe-west1"
}
