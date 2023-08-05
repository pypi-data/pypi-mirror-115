from typing import List

from cloudrail.knowledge.context.azure.network.azure_network_interface import AzureNetworkInterface


class NetworkResource:
    def __init__(self):
        self.network_interfaces: List[AzureNetworkInterface] = []

    @property
    def inbound_connections(self):
        return [inbound_connection for nic in self.network_interfaces for inbound_connection in nic.inbound_connections]

    @property
    def outbound_connections(self):
        return [outbound_connection for nic in self.network_interfaces for outbound_connection in nic.outbound_connections]
