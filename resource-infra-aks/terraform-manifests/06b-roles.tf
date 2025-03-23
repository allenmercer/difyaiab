# Azure Role Assignment Block for AKS to PIP
# https://stackoverflow.com/questions/78190342/with-terraform-how-do-i-integrate-a-basic-sku-load-balancer-and-basic-sku-publi
resource "azurerm_role_assignment" "aks_to_pip_tlb01" {
  description          = "Allows a basic-sku load balancer and basic-sku Public IP integration with an AKS cluster whose load_balancer_sku = basic."
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name = "Network Contributor"
  scope                = azurerm_kubernetes_cluster.aks.node_resource_group_id
  skip_service_principal_aad_check = true
}