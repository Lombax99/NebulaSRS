# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.2"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  skip_provider_registration = "true"
}

data "azurerm_resource_group" "resource_group" {
  name = var.resource_group_name
}

#output "id" {
#  value = data.azurerm_resource_group.resource_group.id
#}

# Create a virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "nebulaVnet"
  address_space       = ["10.0.0.0/16"]
  location            = "westeurope"
  resource_group_name = var.resource_group_name #data.azurerm_resource_group.resource_group.name
}
