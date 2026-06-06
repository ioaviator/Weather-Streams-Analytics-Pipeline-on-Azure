resource "azurerm_resource_group" "event-stream-rg" {
  name     = "evnt-stream-rg"
  location = "East US"
}

resource "azurerm_eventhub_namespace" "envt_hub_stream_ns" {
  name                = "evnt-hub-stream-ns"
  location            = azurerm_resource_group.event-stream-rg.location
  resource_group_name = azurerm_resource_group.event-stream-rg.name
  sku                 = "Standard"
  capacity            = 1

  tags = {
    environment = "Development"
  }
}
