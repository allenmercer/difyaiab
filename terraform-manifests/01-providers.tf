# Terraform Settings Block
terraform {

  required_version = ">=1.10.4"
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.20.0"
    }
  }

  
  backend "azurerm" {
    # The below values will be given in the "terraform init" command.
    # resource_group_name = ""
    # storage_account_name = ""
    # container_name = "tfstate"
    # key = "aks-test.tfstate"
  }
}

# AzureRM Provider Block
provider "azurerm" {
  # The below values are unnecessary because of the "az login" in the pipeline.
  # subscription_id     = ""
  # client_id           = ""
  # client_secret       = ""
  # tenant_id           = ""
  features {
    
  }
}
