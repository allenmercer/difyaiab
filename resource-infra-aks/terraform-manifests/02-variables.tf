# Input variables

# Variables below will be sent and Terraform command line options.

variable "resource_group_name" {
  description = "Resource Group Name"
  # This variable already exists in the pipeline.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}

variable "environment" {
  description = "Environment"
  # This variable already exists in the pipeline.  It can be sent as a Terraform command line option.
  # default = ""
  type = string
}
