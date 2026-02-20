# Terraform outputs

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "environment" {
  description = "Deployment environment"
  value       = var.environment
}

output "region" {
  description = "Deployment region"
  value       = var.region
}

# Storage outputs
output "storage_info" {
  description = "Storage configuration information"
  value = {
    tier           = var.storage_tier
    retention_days = var.storage_retention_days
  }
}

# Database outputs
# output "database_endpoint" {
#   description = "Database connection endpoint"
#   value       = aws_db_instance.main.endpoint
#   sensitive   = true
# }

# Application outputs
# output "api_endpoint" {
#   description = "API endpoint URL"
#   value       = aws_lb.main.dns_name
# }

# Monitoring outputs
# output "monitoring_dashboard_url" {
#   description = "Monitoring dashboard URL"
#   value       = "https://console.aws.amazon.com/cloudwatch/home?region=${var.region}"
# }

output "deployment_timestamp" {
  description = "Timestamp of deployment"
  value       = timestamp()
}
