resource "google_cloud_run_v2_service" "default" {
  name     = "cloudrun-service-v2"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account = "terraform-sa@summarize-398910.iam.gserviceaccount.com"

    containers {
      image = "gcr.io/${var.gcp_project_id}/fastapi-cloudrun:latest"
      env {
        name = "OPENAI_API_KEY"

        value_source {
          secret_key_ref {
            secret  = "openai-api-key"
            version = "latest"
          }
        }
      }
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
    }

    # Include other necessary configurations such as scaling, vpc_access, etc.
  }

  # Traffic configuration
  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  # Additional configurations as needed
}

resource "google_cloud_run_service_iam_member" "public_invoker" {
  location = "us-central1"
  service  = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
