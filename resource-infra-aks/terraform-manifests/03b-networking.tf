# Locals Block
locals {
    # Traefik Load Balancer 01 Public IP Address
    tlb01_ip_name = "pip-${var.project_name}-${var.environment}-${var.location}-${var.project_instance}-tlb01"
}

# Public IP  Block
resource "azurerm_public_ip" "tlb01_public_ip" {
  name                = locals.tlb01_ip_name
  resource_group_name = var.rg_name
  location            = var.location
  allocation_method   = "Static"

  tags = local.tags
}