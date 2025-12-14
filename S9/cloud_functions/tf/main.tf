terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Configurar proveedor de Google Cloud
provider "google" {
  project = var.project_id
  region  = var.region
}
