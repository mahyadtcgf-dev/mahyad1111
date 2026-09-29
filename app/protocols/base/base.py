from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class ProtocolConfig(BaseModel):
    """Base class for protocol-specific configuration parameters."""
    pass

class BaseProtocol(ABC):
    """
    Abstract Base Class for all VPN/Proxy protocols.
    Every protocol handler must implement these methods to be compatible with the ProtocolRegistry.
    """

    @abstractmethod
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new configuration for a user."""
        pass

    @abstractmethod
    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing configuration."""
        pass

    @abstractmethod
    async def delete(self, config_id: str) -> bool:
        """Delete a configuration."""
        pass

    @abstractmethod
    async def validate(self, params: Dict[str, Any]) -> bool:
        """Validate input parameters before creation/update."""
        pass

    @abstractmethod
    def generate_config(self, config_data: Dict[str, Any]) -> str:
        """Generate the raw configuration file content (e.g., for a .conf file)."""
        pass

    @abstractmethod
    def generate_link(self, config_data: Dict[str, Any]) -> str:
        """Generate the URI for the client (e.g., vless://...)."""
        pass

    @abstractmethod
    def generate_qr(self, link: str) -> str:
        """Generate a QR code as Base64 or a URL."""
        pass

    @abstractmethod
    async def get_status(self, config_id: str) -> str:
        """Check the current status of the configuration (Online/Offline)."""
        pass
