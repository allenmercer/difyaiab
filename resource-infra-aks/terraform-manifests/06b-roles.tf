# Azure Role Assignment Block for AKS to PIP
# PIP - https://stackoverflow.com/questions/78190342/with-terraform-how-do-i-integrate-a-basic-sku-load-balancer-and-basic-sku-publi
# Role - https://stackoverflow.com/questions/57753666/terraform-azure-how-to-get-aks-service-principle-object-id
# Azure CLI - https://learn.microsoft.com/en-us/azure/aks/static-ip?source=recommendations#create-a-service-using-the-static-ip-address
resource "azurerm_role_assignment" "aks_to_pip_tlb01" {
  # The kubelet_identity[0].object_id was recommended, but did not work.
  principal_id          = azurerm_kubernetes_cluster.aks.identity[0].principal_id
  role_definition_name = "Network Contributor"
  scope                = data.azurerm_resource_group.rg.id
  # The below was recommenced, but did not work.
  # scope                = azurerm_kubernetes_cluster.aks.node_resource_group_id  
  skip_service_principal_aad_check = true
}