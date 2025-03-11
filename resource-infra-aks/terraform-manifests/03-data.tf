# Terraform Data Blocks

data "azurerm_resource_group" "rg" {
  # name = "${var.rg_name}-${var.environment}"  
  name = var.rg_name
}
