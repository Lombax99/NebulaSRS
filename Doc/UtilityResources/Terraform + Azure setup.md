

[Terraform tutorial](https://developer.hashicorp.com/terraform/tutorials/azure-get-started)
[Azure-cli installation guide](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

nel tutorial di terraform dice che devo associare un ServicePrincipal ma questo non serve davvero, di conseguenza non ho definito nemmeno le variabili di ambiente.

ok, un paio di note, di base non vedo il resource group di srs 2024-stu-g2 
(comando:az group list)

- az account list --output table                                  per stampare le iscrizioni e i loro id
- az account set --subscription sub-id                      per impostare quella iscrizione

dopo aver fatto quei due comandi adesso lo vedo.

Questo è il file.tf che sto provando a lanciare adesso:
```tf
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
}

data "azurerm_resource_group" "resource_group" {
  name     = "srs2024-stu-g2"
  #location = "westeurope"
}

#output "id" {
#  value = data.azurerm_resource_group.resource_group.id
#}
```

e ho ottenuto questo errore:
```
Planning failed. Terraform encountered an error while generating this plan.     
Error: Error ensuring Resource Providers are registered.                         Terraform automatically attempts to register the Resource Providers it supports to ensure it's able to provision resources.                                      If you don't have permission to register Resource Providers you may wish to use the "skip_provider_registration" flag in the Provider block to disable this functionality.

Please note that if you opt out of Resource Provider Registration and Terraform tries to provision a resource from a Resource Provider which is unregistered, then the errors may appear misleading - for example: 
> API version 2019-XX-XX was not found for Microsoft.Foo                         Could indicate either that the Resource Provider "Microsoft.Foo" requires registration, but this could also indicate that this Azure Region doesn't support this API version.

More information on the "skip_provider_registration" flag can be found here:     https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs#skip_provider_registration
```



### Terraform useful commands
Terraform is based on **.tf files**, config files for defining your infrastructure, here are some useful commands:
- **terraform init** to initialize a folder containing a .tf file
	- **-upgrade** if some changes in the .tf require reconfiguration
- **terraform plan** to see what will change with the given .tf file (no changes are applied yet)
- **terraform validate** to see if there are any basic errors in the .tf file
- **terraform apply** to apply and build the infra defined in .tf file
- **terraform destroy** to destroy the infra defined in the .tf file
- **terraform fmt** to format the .tf file for readability and consistency
- **terraform show** to inspect the current state
- **terraform state** has many subcommands, alone will print all the options
	- **list** will print all the resources in the infra

##### Variables
Variables are defined in a different file called variables.tf present in the same directory as the .tf file.

They use the following syntax:
```
variable "var_name" {
  default = "default_value"
}
```

In the config file we call those variables with the following syntax:
```
qualcosa = var.var_name
```

The value can also be defined at runtime with the command
- **terraform apply -var "var_name=value"**

##### Outputs
To define an output for your configuration you need to create a file called output.tf in the same folder as the others and define the output parameter as follow:
``` tf
output "resource_group_id" {
  value = data.azurerm_resource_group.resource_group.id
}
```

The next **terraform apply** will print the defined parameter as output

##### File splitting in Terraform
Terraform does not ascribe any special meaning to which filenames you use and how many files you have. Terraform instead reads all of the `.tf` files and considers their contents together.

Therefore you can freely move the blocks from your `main.tf` file into as many separate `.tf` files in the same directory as you like, and Terraform will consider the configuration to be exactly equivalent as long as you change nothing in the contents of those blocks while you do it.

(There is a special case for [Override Files](https://www.terraform.io/docs/configuration/override.html) that makes the above not strictly true. As long as you avoid naming any of your files `override.tf` or with an `_override.tf` suffix that special case will not apply, but I'm mentioning it just for completeness.)

##### Creating an azure web app
[Esempio 1](https://www.tiernok.com/posts/2021/terraform-for-an-azure-web-app-sql-stack)

##### Creating a postgres database
[microsoft doc](https://learn.microsoft.com/en-us/azure/developer/terraform/deploy-postgresql-flexible-server-database?tabs=azure-cli)
[hashicorp doc](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_database)
[Esempio 1](https://github.com/Azure/terraform-azurerm-postgresql)



