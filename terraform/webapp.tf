# Create the Linux App Service Plan
resource "azurerm_service_plan" "appserviceplan" {
  name                = "NebulaRAT-webapp-asp"
  location            = var.location
  resource_group_name = var.rg_name
  os_type             = "Linux"
  sku_name            = "B1"
}


# Create the web app, pass in the App Service Plan ID
resource "azurerm_linux_web_app" "webapp" {
  name                  = "NebulaRAT-webapp"
  location              = var.location
  resource_group_name   = var.rg_name
  service_plan_id       = azurerm_service_plan.appserviceplan.id
  https_only            = true
  site_config { 
    minimum_tls_version = "1.2"
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = true
    "GOOGLE_USERNAME" = var.google_username
    "GOOGLE_PASSWORD" = var.google_password
    "DB_USERNAME" = var.db_username
    "DB_PASSWORD" = var.db_password
    "DB_HOST" = var.db_host
    "DB_PGDB" = var.db_pgdb
    "FLASK_SECRET" = var.flask_secret
  }
}

#  Deploy code from a public GitHub repo
resource "azurerm_app_service_source_control" "sourcecontrol" {
  app_id             = azurerm_linux_web_app.webapp.id
  repo_url           = "https://github.com/Lombax99/NebulaSRS"
  branch             = "master"
  use_manual_integration = true
  use_mercurial      = false
}
