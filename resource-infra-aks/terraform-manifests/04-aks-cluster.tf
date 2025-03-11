# Locals Block
locals {
    # The location of the Azure Resource Group created for us should be the location for everything.
    location = "${data.azurerm_resource_group.rg.location}"
    log_workspace_name = "log-${var.project_name}-${var.environment}-${locals.location}-${var.project_instance}"
    aks_cluster_name = "aks-${var.project_name}-${var.environment}-${locals.location}-${var.project_instance}"
    node_resource_group = "nrg-${var.project_name}-${var.environment}-${locals.location}-${var.project_instance}"
    nodepool_system_name = "npsystem-${var.project_name}-${var.environment}-${locals.location}-${var.project_instance}"
    nodepool_system_labels = {
      "nodepool-type"       = "system"
      "environment"         = "${var.environment}"
      "nodepoolos"          = "linux"
      "app"                 = "system-apps" 
    }
}

# Azure Kubernetes Service Versions Block
data "azurerm_kubernetes_service_versions" "current" {
  location = locals.location
  include_preview = false
}

# Azure Log Analytics Workspace Block
resource "azurerm_log_analytics_workspace" "insights" {
  name                = locals.log_workspace_name
  location            = locals.location
  resource_group_name = var.rg_name
  retention_in_days   = var.log_retention_days

  tags = var.tags
}

resource "azurerm_kubernetes_cluster" "aks-cluster" {
  name                = locals.aks_cluster_name   
  location            = locals.location
  resource_group_name = var.rg_name
  dns_prefix          = locals.aks_cluster_name
  kubernetes_version = data.azurerm_kubernetes_service_versions.current.latest_version
  node_resource_group = locals.node_resource_group

  default_node_pool {
    name                    = locals.nodepool_system_name
    vm_size                 = "Standard_DS2_v2"
    orchestrator_version    = data.azurerm_kubernetes_service_versions.current.latest_version
    zones                   = var.aks_system_zones
    auto_scaling_enabled    = true
    max_count               = var.aks_system_maxnodes
    min_count               = var.aks_system_minnodes
    os_disk_size_gb         = var.aks_system_disksize
    type                    = "VirtualMachineScaleSets"
    node_labels = locals.nodepool_system_labels
    tags = var.tags
  }

  azure_policy_enabled = true
  
  oms_agent {
    log_analytics_workspace_id= azurerm_log_analytics_workspace.insights.id 
  }

  identity {
    type = "SystemAssigned"
  }

  # Don't know if this is needed or not.
  # Install csi driver.
  key_vault_secrets_provider {
    secret_rotation_enabled = false
  }

  # Don't know what this does.
  lifecycle {
    ignore_changes = [
      default_node_pool.0.node_count, # Ignore due to auto-scaling.
    ]
  }

  linux_profile {
    admin_username = "ubuntu" 
    ssh_key {
      key_data = file(var.ssh_public_key)
    }
  }

  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "standard"
  }

  tags = var.tags
}