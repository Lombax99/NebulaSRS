# Create a virtual network
resource "azurerm_virtual_network" "vnet" {
  name                = "nebulaVnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = var.rg_name #data.azurerm_resource_group.resource_group.name
}

# Create subnet
resource "azurerm_subnet" "my_terraform_subnet" {
  name                 = "mySubnet"
  resource_group_name  = var.rg_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "postgresDB-subnet" {
  name                 = "postgresDB-subnet"
  virtual_network_name = azurerm_virtual_network.vnet.name
  resource_group_name  = var.rg_name
  address_prefixes     = ["10.0.2.0/24"]
  service_endpoints    = ["Microsoft.Storage"]

  delegation {
    name = "fs"

    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action",
      ]
    }
  }
}

resource "azurerm_subnet_network_security_group_association" "postgresDB-sga" {
  subnet_id                 = azurerm_subnet.postgresDB-subnet.id
  network_security_group_id = azurerm_network_security_group.postgresDB-sg.id
}

# Create Network Security Group and rule
resource "azurerm_network_security_group" "my_terraform_nsg" {
  name                = "myNetworkSecurityGroup"
  location            = var.location
  resource_group_name = var.rg_name

  security_rule {
    name                       = "SSH"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_network_security_group" "postgresDB-sg" {
  name                = "postgresDB-nsg"
  location            = var.location
  resource_group_name = var.rg_name

  security_rule {
    name                       = "test123"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}

resource "azurerm_private_dns_zone" "postgresDB-pdns" {
  name                = "postgresDB.postgres.database.azure.com"
  resource_group_name = var.rg_name

  depends_on = [azurerm_subnet_network_security_group_association.postgresDB-sga]
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgresDB-pdns-pdzvnetlink" {
  name                  = "postgresDB-pdzvnetlink.com"
  private_dns_zone_name = azurerm_private_dns_zone.postgresDB-pdns.name
  virtual_network_id    = azurerm_virtual_network.vnet.id
  resource_group_name   = var.rg_name
}
#-----------------------------------------------------------------------------------
# Create public IPs
resource "azurerm_public_ip" "my_terraform_public_ip" {
  name                = "myPublicIP"
  location            = var.location
  resource_group_name = var.rg_name
  allocation_method   = "Dynamic"
}

# Create network interface
resource "azurerm_network_interface" "my_terraform_nic" {
  name                = "myNIC"
  location            = var.location
  resource_group_name = var.rg_name

  ip_configuration {
    name                          = "my_nic_configuration"
    subnet_id                     = azurerm_subnet.my_terraform_subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.my_terraform_public_ip.id
  }
}

# Connect the security group to the network interface
resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.my_terraform_nic.id
  network_security_group_id = azurerm_network_security_group.my_terraform_nsg.id
}

