import json
import subprocess
import os
import logging
from sqlalchemy.orm import Session
from app.database.models import Server, Inbound, Configuration

logger = logging.getLogger("vpn-panel")

class XrayManager:
    """
    Handles the Xray-core process and dynamic configuration generation.
    """
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory
        self.process = None
        self.config_path = "/data/xray/config.json"
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

    def generate_xray_config(self):
        """Reads DB and generates a valid Xray config.json."""
        db = self.db_session_factory()
        try:
            # 1. Fetch all active inbounds and their servers
            inbounds_db = db.query(Inbound).filter(Inbound.is_active == True).all()
            
            xray_inbounds = []
            for ib in inbounds_db:
                server = db.query(Server).filter(Server.id == ib.server_id).first()
                if not server: continue
                
                # Only Xray-compatible protocols
                if ib.protocol not in ["vless", "vmess", "trojan", "shadowsocks"]: continue
                
                #- VLESS/VMess/Trojan implementation
                # For simplicity in Railway, we use the app's port for all WS inbounds
                # and distinguish them by path.
                inbound_config = {
                    "listen": f"0.0.0.0:{ib.port}",
                    "protocol": ib.protocol,
                    "settings": {},
                    "streamSettings": {
                        "network": ib.transport,
                        "security": "tls", # Railway provides TLS at the edge
                        "tlsSettings": {"alpn": ["h2", "http/1.1"]},
                        "wsSettings": {"path": ib.path} if ib.transport == "ws" else {}
                    }
                }
                
                # Add Users (Configurations) for this inbound
                configs = db.query(Configuration).filter(Configuration.inbound_id == ib.id).all()
                
                if ib.protocol == "vless":
                    inbound_config["settings"] = {
                        "clients": [{"id": c.config_data.get("uuid", "0") for c in configs}],
                        "decryption": "none"
                    }
                elif ib.protocol == "vmess":
                    inbound_config["settings"] = {
                        "clients": [{"id": c.config_data.get("uuid", "0") for c in configs}]
                    }
                elif ib.protocol == "trojan":
                    inbound_config["settings"] = {
                        "clients": [{"password": c.config_data.get("password", "password") for c in configs}]
                    }
                
                xray_inbounds.append(inbound_config)

            full_config = {
                "log": {"loglevel": "warning"},
                "inbounds": xray_inbounds,
                "outbounds": [
                    {"protocol": "freedom", "settings": {}},
                    {"protocol": "blackhole", "settings": {}}
                ]
            }
            
            with open(self.config_path, "w") as f:
                json.dump(full_config, f, indent=4)
            
            logger.info(f"Xray config updated at {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate Xray config: {e}")
            return False
        finally:
            db.close()

    def start(self):
        """Starts the Xray process."""
        if self.generate_xray_config():
            try:
                # Start Xray binary
                self.process = subprocess.Popen(
                    ["/usr/local/bin/xray", "run", "-c", self.config_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                logger.info("Xray-core started successfully.")
            except Exception as e:
                logger.error(f"Failed to start Xray binary: {e}")

    def restart(self):
        """Restarts Xray to apply new configurations."""
        logger.info("Restarting Xray-core to apply changes...")
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.start()

    def stop(self):
        """Stops Xray process."""
        if self.process:
            self.process.terminate()
            logger.info("Xray-core stopped.")
