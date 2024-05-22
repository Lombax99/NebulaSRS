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
  name                  = "webapp-terraform"
  location              = var.location
  resource_group_name   = var.rg_name
  service_plan_id       = azurerm_service_plan.appserviceplan.id
  https_only            = true
  site_config { 
    minimum_tls_version = "1.2"
  }
}

/*
####Create a web app
####alwebapp=azurerm_linux_web_app
resource "azurerm_linux_web_app" "linux_webapp" {
  name                = var.web_app_name
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id = azurerm_service_plan.asp.id
  public_network_access_enabled = true
  tags = var.custom_tags

  site_config {
    application_stack {
      java_version = 8
      java_server = "JBOSSEAP"
      java_server_version = "7"
      #To list all the available stacks, run az webapp list-runtimes --linux
    }
  }
}
*/

#  Deploy code from a public GitHub repo
resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id             = azurerm_linux_web_app.webapp.id
  repo_url           = "https://github.com/Azure-Samples/nodejs-docs-hello-world"
  branch             = "master"
  use_manual_integration = true
  use_mercurial      = false
}
