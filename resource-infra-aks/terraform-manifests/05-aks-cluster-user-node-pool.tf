# Locals Block
locals {
    # The location of the Azure Resource Group created for us should be the location for everything.
    nodepool_user_name = "npuser-${var.project_name}-${var.environment}-${local.location}-${var.project_instance}"
    nodepool_user_labels = {
      "nodepool-type" = "user"
      "environment"   = var.environment
      "nodepoolos"    = "linux"
      # Leaving the app label the project name for now.
      # We could create root varialbes for different node pools so that the pools would be assigned to that specific app.
      # For now, this is not necessary.
      "app"           = var.project_name
    }
}

# Azure Kubernetes Cluster Linux Node Pool Block
resource "azurerm_kubernetes_cluster_node_pool" "aksnp001" {
  zones    = var.aks_user_zones
  auto_scaling_enabled   = true
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id    
  max_count             = var.aks_user_maxnodes
  min_count             = var.aks_user_minnodes
  mode                  = "User"
  name                  = local.nodepool_user_name
  orchestrator_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  os_disk_size_gb       = var.aks_user_disksize
  os_type               = "Linux" # Default is Linux, we can change to Windows
  vm_size               = var.aks_user_vmsize
  priority              = "Regular"  # Default is Regular, we can change to Spot with additional settings like eviction_policy, spot_max_price, node_labels and node_taints
  node_labels = local.nodepool_user_labels
  tags = var.tags
}
