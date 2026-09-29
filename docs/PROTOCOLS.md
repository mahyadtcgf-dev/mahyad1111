# Protocol Specification

## 1. Protocol Registry
A central `ProtocolRegistry` manages all supported networking protocols.

### Registry Interface
- `register(protocol_instance)`: Adds a protocol to the system.
- `get(protocol_name)`: Retrieves a protocol handler.
- `list()`: Returns all registered protocols.
- `is_supported(protocol_name)`: Boolean check.

## 2. Protocol Interface (Abstract Base Class)
Every protocol must implement the following methods:
- `create(user_id, params)`: Creates a new configuration.
- `update(config_id, params)`: Modifies an existing configuration.
- `delete(config_id)`: Removes the configuration.
- `enable/disable(config_id)`: Toggles active status.
- `validate(params)`: Validates input parameters.
- `generate_config()`: Returns the raw configuration file content.
- `generate_link()`: Returns the URI for the client (e.g., `vless://...`).
- `generate_qr()`: Returns a QR code as an image or Base64.
- `get_status()`: Checks if the configuration is currently reachable/valid.

## 3. Supported Protocols

### Xray-core Protocols (Primary Focus)
- **VLESS:** WebSocket, gRPC, xHTTP.
- **VMess:** WebSocket, TCP.
- **Trojan:** WebSocket, HTTPUpgrade.
- **Shadowsocks:** AEAD (aes-256-gcm).

## 4. Runtime Status Matrix

| Protocol | Config Gen | Runtime | Railway Compatibility | Status |
|----------|-------------|---------|-------------------------|--------|
| VLESS    | ✅ | ✅ | High (via WebSocket/TCP) | SUPPORTED |
| VMess    | ✅ | ✅ | High | SUPPORTED |
| Trojan   | ✅ | ✅ | High | SUPPORTED |
| SS       | ✅ | ✅ | High | SUPPORTED |
| WireGuard | ⏳ | ❌ | Not Supported | DEFERRED |
