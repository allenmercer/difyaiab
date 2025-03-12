# Input variables

locals {
  tags = {
    # BEGIN ST TAGS
    creator = "terraform"
    workloadtier = "infrastructure"
    customer = "ailevate"
    # END ST TAGS
    environment = var.environment
    workload = var.project_name
  }
}

# Variables that should be set before deployment.

variable "log_retention_days" {
  description = "Azure Log Analytics Workspace Log Retention Days"
  default = 30
  type = number
}

variable "aks_system_vmsize" {
  description = "Node size for VMs in the AKS System Pool"
  default = "Standard_DS2_v2"
  type = string
}

variable "aks_system_zones" {
  description = "Zones for VMs in the AKS System Pool"
  default = [1, 2]
  type = list
}

variable "aks_system_minnodes" {
  description = "Minimum Number of Nodes for AKS System Pool Scaling Set"
  default = 1
  type = number
}

variable "aks_system_maxnodes" {
  description = "Maximum Number of Nodes for AKS System Pool Scaling Set"
  default = 3
  type = number
}

variable "aks_system_disksize" {
  description = "Disk Size for Nodes for AKS System Pool"
  default = 30
  type = number
}

variable "aks_user_vmsize" {
  description = "Node size for VMs in the AKS User Pool"
  default = "Standard_DS2_v2"
  type = string
}

variable "aks_user_zones" {
  description = "Zones for VMs in the AKS User Pool"
  default = [1, 2]
  type = list
}

variable "aks_user_minnodes" {
  description = "Minimum Number of Nodes for AKS User Pool Scaling Set"
  default = 1
  type = number
}

variable "aks_user_maxnodes" {
  description = "Maximum Number of Nodes for AKS User Pool Scaling Set"
  default = 3
  type = number
}

variable "aks_user_disksize" {
  description = "Disk Size for Nodes for AKS User Pool"
  default = 30
  type = number
}

# Moved to locals
#variable "tags" {
#  type = map(string)
#  default = {
#    # BEGIN MANDATORY TAGS
#    creator = "terraform"
#    workloadtier = "infrastructure"
#    customer = "ailevate"
#    environment = "poc"
#    workload = "difyaiab"
#    # END MANDATORY TAGS
#  }
#}

# Variables below will be sent and Terraform command line options.

variable "rg_name" {
  description = "Resource Group Name"
  # This variable already exists in the pipeline as AZURE_RG_NAME.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}

variable "environment" {
  description = "Environment"
  # This variable already exists in the pipeline as LIFECYCLE_ENVIRONMENT.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}

variable "project_name" {
  description = "Project Name"
  # This variable already exists in the pipeline as AZURE_PROJECT_NAME.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}

variable "project_instance" {
  description = "Project Instance"
  # This variable already exists in the pipeline AZURE_PROJECT_INSTANCE.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}

# SSH Public Key for Linux VMs.
variable "ssh_public_key" {
  # This variable already exists in the pipeline as sshkey.  It can be sent as a Terraform command line option.
  description = "This variable defines the SSH Public Key for Linux k8s Worker nodes"  
}