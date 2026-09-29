# Architecture Specification

## 1. Technology Stack

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **Asynchronous Engine:** `asyncio`
- **Database:** PostgreSQL (Production), SQLite (Development)
- **Caching/Rate Limiting:** Redis (Optional/Abstracted)
- **Task Queue:** Background Tasks (FastAPI) or Celery (if scaled)

### Frontend
- **Framework:** React 18+
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Library:** Headless UI / Radix UI (for accessibility)
- **State Management:** React Query (TanStack Query)
- **Directionality:** RTL (Primary: Persian)

## 2. High-Level Architecture

The system follows a **Modular Monolith** approach to maintain simplicity for Railway deployment while allowing for future micro-service extraction.

### Components
- **API Gateway (FastAPI):** Handles authentication, RBAC, and request routing.
- **Protocol Engine:** A registry-based system where each protocol (WireGuard, VLESS, etc.) implements a standard interface for config generation and status checking.
- **Subscription Engine:** Generates cryptographically secure tokens and serves configuration lists in various formats (Base64, JSON, Text).
- **Traffic Manager:** Tracks bandwidth usage per user/link and enforces quotas.
- **Monitoring Service:** Periodically polls server health and resource usage.
- **Frontend (React):** An RTL dashboard for Admin and a public-facing subscription page for Users.

## 3. Data Flow
1. **Admin Request:** Admin creates a user $\rightarrow$ API $\rightarrow$ Database $\rightarrow$ Protocol Engine $\rightarrow$ Configuration generated $\rightarrow$ stored in DB.
2. **User Request:** Client hits `/sub/{token}` $\rightarrow$ Subscription Engine $\rightarrow$ Validates Token $\rightarrow$ Fetches configs from DB $\rightarrow$ Serializes for client $\rightarrow$ returns response.
3. **Traffic Update:** Server reports usage $\rightarrow$ Traffic Manager $\rightarrow$ Updates DB $\rightarrow$ Trigger notification if threshold reached.

## 4. Deployment Strategy
- **Platform:** Railway.app
- **Containerization:** Multi-stage Dockerfile (Python slim).
- **Persistence:** Railway Volumes for SQLite (dev) or Managed PostgreSQL (prod).
- **Network:** Port 80/443 exposed via Railway Domain.
