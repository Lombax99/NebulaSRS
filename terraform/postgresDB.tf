resource "azurerm_postgresql_flexible_server" "postgresDB-FlexServer" {
  name                   = "nebularat-postgresdb-server"
  resource_group_name    = var.rg_name
  location               = var.location
  version                = "13"
  #delegated_subnet_id    = azurerm_subnet.postgresDB-subnet.id
  #private_dns_zone_id    = azurerm_private_dns_zone.postgresDB-pdns.id
  
  administrator_login    = var.db_username
  administrator_password = var.db_password
  
  zone                   = "1"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  backup_retention_days  = 7

  #depends_on = [azurerm_private_dns_zone_virtual_network_link.postgresDB-pdns-pdzvnetlink]
}

resource "azurerm_postgresql_flexible_server_database" "postgresDB-server-database" {
  name      = "nebularat-postgresServer-db"
  server_id = azurerm_postgresql_flexible_server.postgresDB-FlexServer.id
  collation = "en_US.utf8"
  charset   = "UTF8"
}

resource "azurerm_postgresql_flexible_server_firewall_rule" "postgresDB-FlexServer-firewall-rules" {
  name             = "postgresDB-FlexServer-fw"
  server_id        = azurerm_postgresql_flexible_server.postgresDB-FlexServer.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "255.255.255.255"
}

