resource "azurerm_postgresql_flexible_server" "postgresDB-FlexServer" {
  name                   = "postgresdb-server"
  resource_group_name    = var.rg_name
  location               = var.location
  version                = "13"
  delegated_subnet_id    = azurerm_subnet.postgresDB-subnet.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgresDB-pdns.id
  
  administrator_login    = "adminTerraform"
  administrator_password = "password"
  
  zone                   = "1"
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2s_v3"
  backup_retention_days  = 7

  depends_on = [azurerm_private_dns_zone_virtual_network_link.postgresDB-pdns-pdzvnetlink]
}

resource "azurerm_postgresql_flexible_server_database" "postgresDB-server-database" {
  name      = "postgresServer-db"
  server_id = azurerm_postgresql_flexible_server.postgresDB-FlexServer.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}



/* This was the version given from the hashicorp doc, what's is the difference with the flexible server?
resource "azurerm_postgresql_server" "postgresDB" {
  name                = "psqlserver"
  location            = var.location
  resource_group_name = var.rg_name

  administrator_login          = "psqladmin"
  administrator_login_password = "H@Sh1CoR3!"

  sku_name   = "GP_Gen5_4"
  version    = "11"
  storage_mb = 10240

  backup_retention_days        = 7
  #geo_redundant_backup_enabled = true
  auto_grow_enabled            = true

  public_network_access_enabled    = false
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"
}
*/

