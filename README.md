# Professional VPN Management Panel

A production-ready VPN Control Panel built with FastAPI, PostgreSQL, Redis, and React, optimized for deployment on Railway.app.

## 🏗 Architecture

The system follows a **Control Plane / Data Plane** separation:
- **Control Plane (Railway)**: Manages users, subscriptions, nodes, and configuration generation.
- **Data Plane (VPN Nodes)**: Independent servers running Xray-core/WireGuard that handle actual VPN traffic.

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy (PostgreSQL), Redis, Pydantic.
- **Frontend**: React, TypeScript, Vite, Tailwind CSS.
- **Deployment**: Docker, Railway.app.

## 🚀 Deployment to Railway

1. **Create Railway Project**:
   - Add a **PostgreSQL** database.
   - Add a **Redis** instance.
   - Deploy the **Web Service** from this repository.

2. **Environment Variables**:
   Set the following variables in the Railway Dashboard:
   - `DATABASE_URL`: Provided by Railway PostgreSQL.
   - `REDIS_URL`: Provided by Railway Redis.
   - `JWT_SECRET`: A long, random string.
   - `PUBLIC_DOMAIN`: Your Railway app domain (e.g., `vpn-panel.up.railway.app`).
   - `PORT`: (Automatic) Railway injects this.

3. **Healthcheck**:
   Railway will use the `/health` and `/ready` endpoints to verify deployment.

## 🛠 Adding a VPN Node

To connect a node to the panel:
1. **Register Node**: Use the Admin Panel $ightarrow$ Nodes $ightarrow$ Add Node.
2. **Node Agent**: Install the node agent on your server.
3. **Heartbeat**: The node will start sending heartbeats to `https://<panel-domain>/heartbeat/` containing CPU/RAM/Traffic metrics.
4. **Management**: The panel communicates with the node via a management API (or gRPC) to add/remove users in real-time.

## 🔑 User & Config Flow
1. **User Creation**: Admin creates a user $ightarrow$ User gets a subscription.
2. **Config Generation**: Admin/User selects a Node + Protocol $ightarrow$ Panel requests Node to create user $ightarrow$ Panel generates a valid `vless://` or `vmess://` link.
3. **Connection**: User imports the link into their client (e.g., v2rayN, Shadowrocket).

## 🛡 Security Hardening
- **RBAC**: Granular permissions (`SUPER_ADMIN`, `ADMIN`, `OPERATOR`, `USER`).
- **JWT**: Short-lived access tokens + Rotating refresh tokens.
- **CORS**: Restricted to defined origins.
- **Input Validation**: Strict Pydantic schemas for all API requests.
- **Network**: Private internal DNS for DB/Redis communication.
