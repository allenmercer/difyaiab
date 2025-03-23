# Locals Block
locals {
    container_registry_name = "cr${var.project_name}${var.environment}${var.location}${var.project_instance}"
}

# Azure Container Registry Block
# Admin can also be added with: az acr update -n crdifyaipoc001 --admin-enabled true
resource "azurerm_container_registry" "cr" {
  name                = local.container_registry_name
  resource_group_name = var.rg_name
  location            = var.location
  sku                 = "Premium"
  admin_enabled       = true
  tags = local.tags
}

# Azure Role Assignment Block for AKS to CR
# May also need to use: az aks update -n difyai-agent-builder-poc-cluster -g difyai-agent-builder-poc --attach-acr crdifyaipoc001
resource "azurerm_role_assignment" "aks-to-cr" {
  principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.cr.id
  skip_service_principal_aad_check = true
}