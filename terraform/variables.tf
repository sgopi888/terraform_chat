variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud project ID"
}

variable "gcp_region" {
  type        = string
  description = "The GCP region"
  default     = "us-central1"
}

variable "gcp_credentials_file" {
  type        = string
  description = "Path to the GCP credentials JSON file"
}

variable "gcp_network_name" {
  type        = string
  description = "The name of the VPC network"
  default     = "default"
}

variable "gcp_services" {
  type        = list(string)
  description = "List of GCP services to enable"
}

variable "gcp_service_account_name" {
  type        = string
  description = "The name of the service account"
}

variable "gcp_project_number" {
  type        = string
  description = "The GCP project number"
}

# --- FINANCIAL GUARDRAIL ---
variable "enable_expensive_index" {
  type        = bool
  description = "Set to true ONLY during active testing to avoid high costs ($0.30/hr)"
  default     = false
}

variable "gcp_zone" {
  description = "Zone"
  type        = string
}

variable "branch" {
  description = "Git branch"
  type        = string
}