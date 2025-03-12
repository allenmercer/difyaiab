output "latest_version" {
  value = data.azurerm_kubernetes_service_versions.current.latest_version
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_cluster_k8s_version" {
  value = azurerm_kubernetes_cluster.aks.kubernetes_version
}

output "cr_login_server" {
  value = azurerm_container_registry.cr.login_server
}
