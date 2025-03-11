output "latest_version" {
  value = data.azurerm_kubernetes_service_versions.current.latest_version
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks-cluster.name
}

output "aks_cluster_k8s_version" {
  value = azurerm_kubernetes_cluster.aks-cluster.kubernetes_version
}