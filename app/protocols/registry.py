from typing import Dict, Type, Optional
import logging
from app.protocols.base.base import BaseProtocol

logger = logging.getLogger(__name__)

class ProtocolRegistry:
    """
    Central registry for managing and accessing supported protocols.
    Implements the Singleton pattern.
    """
    _instance = None
    _protocols: Dict[str, BaseProtocol] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProtocolRegistry, cls).__new__(cls)
        return cls._instance

    def register(self, name: str, protocol_handler: BaseProtocol):
        """Registers a protocol handler."""
        self._protocols[name.lower()] = protocol_handler
        logger.info(f"Protocol '{name}' registered successfully.")

    def get(self, name: str) -> Optional[BaseProtocol]:
        """Retrieves a registered protocol handler."""
        return self._protocols.get(name.lower())

    def list_protocols(self) -> List[str]:
        """Lists all registered protocols."""
        return list(self._protocols.keys())

    def is_supported(self, name: str) -> bool:
        """Checks if a protocol is supported."""
        return name.lower() in self._protocols

# Global instance for easy import
registry = ProtocolRegistry()
