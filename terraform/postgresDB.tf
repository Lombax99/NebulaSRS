resource "azurerm_postgresql_flexible_server" "postgresDB-FlexServer" {
  name                   = "postgresdb-server"
  resource_group_name    = var.rg_name
  location               = var.location
  version                = "13"
  delegated_subnet_id    = azurerm_subnet.postgresDB-subnet.id
  private_dns_zone_id    = azurerm_private_dns_zone.postgresDB-pdns.id
  
  administrator_login    = "sudo"
  administrator_password = "sudo"
  
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

