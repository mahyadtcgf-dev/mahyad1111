import uuid
import base64
import json
from typing import Any, Dict
from app.protocols.base.base import BaseProtocol
from app.core.node_manager import node_manager
from app.database.models import Server

class XrayProtocol(BaseProtocol):
    """Helper base class for Xray-core based protocols (VLESS, VMess, Trojan, SS)."""
    
    def generate_qr(self, link: str) -> str:
        return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={link}"

    async def _dispatch_to_node(self, server: Server, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Private helper to send commands to the node via NodeManager."""
        return await node_manager.send_command(server, command, params)

class VLESSProtocol(XrayProtocol):
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not isinstance(server, Server):
            return {"status": "error", "message": "Server object required in params"}
        
        u_id = params.get("uuid", str(uuid.uuid4()))
        # Dispatch to node to actually create the user in Xray config
        result = await self._dispatch_to_node(server, "add_vless_user", {"uuid": u_id, "email": user_id})
        
        if result.get("status") == "error":
            return result
            
        return {"uuid": u_id, "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not server: return {"status": "error", "message": "Server required"}
        return await self._dispatch_to_node(server, "update_vless_user", params)

    async def delete(self, config_id: str) -> bool:
        server = params.get("server")
        if not server: return False
        result = await self._dispatch_to_node(server, "delete_vless_user", {"id": config_id})
        return result.get("status") == "success"

    async def validate(self, params: Dict[str, Any]) -> bool:
        return "endpoint" in params and "port" in params

    def generate_config(self, config_data: Dict[str, Any]) -> str:
        return json.dumps({"protocol": "vless", "settings": config_data}, indent=2)

    def generate_link(self, config_data: Dict[str, Any]) -> str:
        u_id = config_data.get("uuid")
        host = config_data.get("endpoint")
        port = config_data.get("port")
        label = config_data.get("label", "ProfessionalVPN")
        return f"vless://{u_id}@{host}:{port}?security=tls&encryption=none&type=ws# {label}"

    async def get_status(self, config_id: str) -> str:
        return "ONLINE"

class TrojanProtocol(XrayProtocol):
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not server: return {"status": "error", "message": "Server required"}
        
        pwd = params.get("password", "password123")
        result = await self._dispatch_to_node(server, "add_trojan_user", {"password": pwd, "email": user_id})
        
        if result.get("status") == "error": return result
        return {"password": pwd, "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not server: return {"status": "error", "message": "Server required"}
        return await self._dispatch_to_node(server, "update_trojan_user", params)

    async def delete(self, config_id: str) -> bool:
        server = params.get("server")
        if not server: return False
        result = await self._dispatch_to_node(server, "delete_trojan_user", {"id": config_id})
        return result.get("status") == "success"

    async def validate(self, params: Dict[str, Any]) -> bool:
        return "endpoint" in params

    def generate_config(self, config_data: Dict[str, Any]) -> str:
        return json.dumps({"protocol": "trojan", "settings": config_data}, indent=2)

    def generate_link(self, config_data: Dict[str, Any]) -> str:
        pwd = config_data.get("password")
        host = config_data.get("endpoint")
        port = config_data.get("port")
        label = config_data.get("label", "ProfessionalVPN")
        return f"trojan://{pwd}@{host}:{port}?security=tls# {label}"

    async def get_status(self, config_id: str) -> str:
        return "ONLINE"

class VMessProtocol(XrayProtocol):
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not server: return {"status": "error", "message": "Server required"}
        
        u_id = str(uuid.uuid4())
        result = await self._dispatch_to_node(server, "add_vmess_user", {"uuid": u_id, "email": user_id})
        
        if result.get("status") == "error": return result
        return {"uuid": u_id, "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        server = params.get("server")
        if not server: return {"status": "error", "message": "Server required"}
        return await self._dispatch_to_node(server, "update_vmess_user", params)

    async def delete(self, config_id: str) -> bool:
        server = params.get("server")
        if not server: return False
        result = await self._dispatch_to_node(server, "delete_vmess_user", {"id": config_id})
        return result.get("status") == "success"

    async def validate(self, params: Dict[str, Any]) -> bool:
        return "endpoint" in params

    def generate_config(self, config_data: Dict[str, Any]) -> str:
        return json.dumps({"protocol": "vmess", "settings": config_data}, indent=2)

    def generate_link(self, config_data: Dict[str, Any]) -> str:
        vmess_json = {
            "v": "2",
            "ps": config_data.get("label", "ProfessionalVPN"),
            "add": config_data.get("endpoint"),
            "port": config_data.get("port"),
            "id": config_data.get("uuid"),
            "aid": "0",
            "scy": "auto",
            "net": "ws",
            "type": "none",
            "host": config_data.get("endpoint"),
            "path": "/vmesse",
            "tls": "tls"
        }
        encoded = base64.b64encode(json.dumps(vmess_json).encode()).decode()
        return f"vmess://{encoded}"

    async def get_status(self, config_id: str) -> str:
        return "ONLINE"
