terraform {
  required_providers {
    google = {
      source = "hashicorp/google"

    }
    google-beta = {
      source = "hashicorp/google-beta"

    }
  }
}

provider "google" {
  credentials = file(var.gcp_credentials_file)
  project     = var.gcp_project_id
  region      = var.gcp_region
  zone        = var.gcp_zone
}

provider "google-beta" {
  credentials = file(var.gcp_credentials_file)
  project     = var.gcp_project_id
  region      = var.gcp_region
  zone        = var.gcp_zone
}

# Fetch existing service account
data "google_service_account" "existing_service_account" {
  account_id = var.gcp_service_account_name
}

resource "google_project_iam_member" "existing_service_account_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/discoveryengine.admin"
  ])

  project = var.gcp_project_id
  role    = each.value
  member  = "serviceAccount:${data.google_service_account.existing_service_account.email}"
}

# Activate Google services
resource "google_project_service" "enabled_services" {
  for_each           = toset(var.gcp_services)
  service            = each.key
  disable_on_destroy = false
}



# IAM role assignments for an existing service account
# resource "google_project_iam_member" "existing_service_account_iam_roles" {
# for_each = toset(var.gcp_existing_service_account_roles)
# project  = var.gcp_project_id
# role     = "roles/${each.value}"
# member   = "serviceAccount:${data.google_service_account.existing_service_account.email}"
# }

# IAM role assignments for Cloud Build service account with specific roles
# resource "google_project_iam_member" "cloud_build_service_account_iam_roles" {
# for_each = toset(var.gcp_cloud_build_service_account_roles)
# project  = var.gcp_project_id
# role     = "roles/${each.value}"
# member   = "serviceAccount:${var.gcp_project_number}@cloudbuild.gserviceaccount.com"
# }



/* -------------------------------------------------------------------------- */
/*                                   Modules                                  */
/* -------------------------------------------------------------------------- */

#module "secret_manager" {
# source       = "./modules/secret_manager"
# github_token = var.github_token
#}



module "cloud_run" {
  source = "./modules/cloud_run"

  gcp_project_id = var.gcp_project_id
  gcp_region     = var.gcp_region
  network_id     = var.gcp_network_name
}

# --- PHASE 2.3: INGESTION (SAFE - PENNIES) ---

# 1. The GCS Landing Zone
resource "google_storage_bucket" "dataset_bucket" {
  name     = "${var.gcp_project_id}-dataset-bucket"
  location = var.gcp_region
  force_destroy = true # Good for learning POCs so terraform destroy works clean
}

# 2. Automated Sync (Syncing your local PDFs to the cloud)
resource "google_storage_bucket_object" "upload_pdfs" {
  for_each = fileset("../backend/dataset/", "*.pdf")

  name   = "dataset/${each.value}"
  source = "../backend/dataset/${each.value}"
  bucket = google_storage_bucket.dataset_bucket.name
}

# --- HIGH COST GUARDRAIL ---

# 1. The Index (The math/vectors)
resource "google_vertex_ai_index" "quiz_index" {
  count        = var.enable_expensive_index ? 1 : 0
  display_name = "quiz-index"
  description  = "Vector index for RAG"
  region       = var.gcp_region

  metadata {
    # ✅ Link to the bucket created above
    contents_delta_uri = "gs://${google_storage_bucket.dataset_bucket.name}/index/"
    config {
      dimensions                  = 768 # Standard for Vertex embeddings
      approximate_neighbors_count = 150
      distance_measure_type       = "DOT_PRODUCT_DISTANCE"
      algorithm_config {
        tree_ah_config {
          leaf_node_embedding_count    = 500
          leaf_nodes_to_search_percent = 7
        }
      }
    }
  }
  index_update_method = "STREAM_UPDATE"
}

# 2. The Endpoint (The expensive VM runner $$$)
resource "google_vertex_ai_index_endpoint" "quiz_endpoint" {
  count        = var.enable_expensive_index ? 1 : 0
  display_name = "quiz-index-endpoint"
  description  = "EXPERIMENTAL ENDPOINT - DESTROY AFTER TEST"
  region       = var.gcp_region

  public_endpoint_enabled = true
}
