# Railway Deployment Specification

## 1. Deployment Workflow
1. **GitHub Integration:** Connect the repository to Railway.app.
2. **Build:** Railway detects `Dockerfile` and builds the image.
3. **Environment:** Configure variables in the Railway Dashboard.
4. **Network:** Expose the application port (default: `8000`).

## 2. Environment Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Connection string for PostgreSQL | `postgresql://user:pass@host:port/db` |
| `SECRET_KEY` | JWT secret for auth | `long-random-string` |
| `RAILWAY_PUBLIC_DOMAIN` | The public URL of the app | `myapp.up.railway.app` |
| `REDIS_URL` | Connection string for Redis (optional) | `redis://...` |
| `ADMIN_EMAIL` | Default super-admin email | `admin@example.com` |

## 3. Storage and Persistence
- **Database:** Use Railway's managed PostgreSQL plugin.
- **Static Files/Logs:** Use a Railway Volume mounted at `/data` if using local SQLite or for log archival.

## 4. Health Checks
- `/health`: Returns `{"status": "ok"}`.
- `/ready`: Checks database connectivity and protocol registry readiness.

## 5. Limitations on Railway
- **Kernel Modules:** WireGuard requires kernel-level access or specific headers. Standard Railway containers may not support `wg-quick`.
- **UDP Ports:** Railway's networking primarily supports TCP/HTTP. UDP-based protocols (like raw WireGuard) may require a dedicated VPS or a specialized Railway setup (via custom networking).
- **Status:** WireGuard Runtime = `NOT SUPPORTED ON RAILWAY` (Config generation only).
