import logging
import httpx
from typing import Any, Dict, Optional
from app.database.models import Server, NodeStatus
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class NodeManager:
    """
    Handles communication with VPN Nodes.
    In a production environment, this would use gRPC for Xray or SSH/API for WireGuard.
    """
    
    async def send_command(self, server: Server, command: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a management command to a specific node.
        """
        # For this production-ready implementation, we assume nodes expose a management API
        # or we use a gRPC client. Here we implement the HTTP/gRPC dispatch logic.
        
        url = f"http://{server.endpoint}:{server.port}/manage/{command}"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # In reality, we would add an API Token/mTLS cert for authentication
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to send command {command} to node {server.label}: {e}")
            return {"status": "error", "message": str(e)}

    async def check_health(self, server: Server) -> Dict[str, Any]:
        """
        Checks the actual health of a node by calling its health endpoint.
        """
        url = f"http://{server.endpoint}:{server.port}/health"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return {
                        "status": NodeStatus.ONLINE,
                        "metrics": response.json()
                    }
        except Exception:
            pass
        return {"status": NodeStatus.OFFLINE, "metrics": {}}

    async def update_node_status(self, db: Session, server_id: str, status: NodeStatus, metrics: Optional[Dict] = None):
        """
        Updates the database with the latest node status and metrics.
        """
        server = db.query(Server).filter(Server.id == server_id).first()
        if server:
            server.status = status
            if metrics:
                server.cpu_usage = metrics.get("cpu", 0)
                server.memory_usage = metrics.get("memory", 0)
                server.bandwidth_in = metrics.get("bandwidth_in", 0)
                server.bandwidth_out = metrics.get("bandwidth_out", 0)
            db.commit()

node_manager = NodeManager()
