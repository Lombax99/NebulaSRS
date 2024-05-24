

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
[Esempio 2](https://medium.com/@abhimanyubajaj98/your-first-azure-web-app-with-terraform-f8ef567f206b)
[microsoft doc](https://learn.microsoft.com/it-it/azure/app-service/provision-resource-terraform)

##### Configure auto deploy from github
In [this tutorial](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli) a simple web app is given and deployed via local github, we want remote github deployment but it's better than nothing for now.

SCM basic auth publishing credential need to be activate in some way, might become a problem with terraform configuration later

OK sono riuscito, questo è il file di terraform:
```
# Create the Linux App Service Plan
resource "azurerm_service_plan" "appserviceplan" {
  name                = "webapp-asp-terraform"
  location            = var.location
  resource_group_name = var.rg_name
  os_type             = "Linux"
  sku_name            = "B1"
}


# Create the web app, pass in the App Service Plan ID
resource "azurerm_linux_web_app" "webapp" {
  name                  = "webapp124-terraform"
  location              = var.location
  resource_group_name   = var.rg_name
  service_plan_id       = azurerm_service_plan.appserviceplan.id
  https_only            = true
  site_config { 
    minimum_tls_version = "1.2"
    application_stack {
    	python_version = 3.9
    }
  }
}

#  Deploy code from a public GitHub repo
resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id             = azurerm_linux_web_app.webapp.id
  repo_url           = "https://github.com/Lombax99/basic-flask-webapp"
  branch             = "master"
  use_manual_integration = true
  use_mercurial      = false
}
```

e questo è il file di github:

```
# Docs for the Azure Web Apps Deploy action: https://github.com/Azure/webapps-deploy
# More GitHub Actions for Azure: https://github.com/Azure/actions
# More info on Python, GitHub Actions, and Azure App Service: https://aka.ms/python-webapps-actions

name: Build and deploy Python app to Azure Web App - basic-webapp-to-test-git-deployment

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python version
        uses: actions/setup-python@v1
        with:
          python-version: '3.9'

      - name: Create and start virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate
      
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      # Optional: Add step to run tests here (PyTest, Django test suites, etc.)

      - name: Zip artifact for deployment
        run: zip release.zip ./* -r

      - name: Upload artifact for deployment jobs
        uses: actions/upload-artifact@v3
        with:
          name: python-app
          path: |
            release.zip
            !venv/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'Production'
      url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}
    
    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v3
        with:
          name: python-app

      - name: Unzip artifact for deployment
        run: unzip release.zip

      
      - name: 'Deploy to Azure Web App'
        uses: azure/webapps-deploy@v2
        id: deploy-to-webapp
        with:
          app-name: 'webapp124-terraform'
          slot-name: 'Production'
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_124 }}
```

Ho dovuto preparare github un minimo per avere le azioni che fanno il deployment.
Due punti fondamentali:
- una variabile da definire come segreto su github
	`publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE_124 }}`
	repo settings > secret and variables > action > create new
	the value is defined in azure, from the home page: Download publish profile and copy the falue from the file in the variable on github
- `app-name: 'webapp124-terraform'` che deve contenere il nome giusto di azure

##### Creating a postgres database
[microsoft doc](https://learn.microsoft.com/en-us/azure/developer/terraform/deploy-postgresql-flexible-server-database?tabs=azure-cli)
[hashicorp doc](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/postgresql_database)
[Esempio 1](https://github.com/Azure/terraform-azurerm-postgresql)



