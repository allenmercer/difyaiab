# Terraform Data Retreival

data "azurerm_resource_group" "rg" {
  # name = "${var.resource_group_name}-${var.environment}"  
  name = "${var.resource_group_name}
}
