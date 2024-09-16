terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.91.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "turplanlegger-terraform-rg"
    storage_account_name = "turplanleggerterraformst"
    container_name       = "state"
    key                  = "turplanlegger-fastapi.tfstate"
  }
}

provider "azurerm" {
  features {}
}
