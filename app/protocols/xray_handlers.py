import uuid
import base64
import json
from typing import Any, Dict
from app.protocols.base.base import BaseProtocol

class XrayProtocol(BaseProtocol):
    """Helper base class for Xray-core based protocols (VLESS, VMess, Trojan, SS)."""
    
    def generate_qr(self, link: str) -> str:
        # In a real app, use a QR library. For now, return a placeholder or a link to an API.
        return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={link}"

class VLESSProtocol(XrayProtocol):
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        # VLESS requires a UUID
        u_id = params.get("uuid", str(uuid.uuid4()))
        return {"uuid": u_id, "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "updated"}

    async def delete(self, config_id: str) -> bool:
        return True

    async def validate(self, params: Dict[str, Any]) -> bool:
        return "endpoint" in params and "port" in params

    def generate_config(self, config_data: Dict[str, Any]) -> str:
        # Xray JSON format
        return json.dumps({"protocol": "vless", "settings": config_data}, indent=2)

    def generate_link(self, config_data: Dict[str, Any]) -> str:
        # vless://uuid@host:port?query#label
        u_id = config_data.get("uuid")
        host = config_data.get("endpoint")
        port = config_data.get("port")
        label = config_data.get("label", "ProfessionalVPN")
        return f"vless://{u_id}@{host}:{port}?security=tls&encryption=none&type=ws# {label}"

    async def get_status(self, config_id: str) -> str:
        return "ONLINE"

class TrojanProtocol(XrayProtocol):
    async def create(self, user_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"password": params.get("password", "password123"), "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "updated"}

    async def delete(self, config_id: str) -> bool:
        return True

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
        return {"uuid": str(uuid.uuid4()), "status": "created"}

    async def update(self, config_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "updated"}

    async def delete(self, config_id: str) -> bool:
        return True

    async def validate(self, params: Dict[str, Any]) -> bool:
        return "endpoint" in params

    def generate_config(self, config_data: Dict[str, Any]) -> str:
        return json.dumps({"protocol": "vmess", "settings": config_data}, indent=2)

    def generate_link(self, config_data: Dict[str, Any]) -> str:
        # VMess uses a Base64 encoded JSON
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
