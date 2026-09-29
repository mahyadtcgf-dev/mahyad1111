# Security Specification

## 1. Authentication
- **Admin Auth:** JWT-based session management.
- **Password Hashing:** Argon2 or bcrypt.
- **Cookies:** `HttpOnly`, `Secure`, `SameSite=Strict`.
- **2FA:** TOTP (Time-based One-Time Password) using `pyotp`.

## 2. Authorization (RBAC)
The system uses Role-Based Access Control with the following roles:
- `SUPER_ADMIN`: Full system access.
- `ADMIN`: Manage users, servers, and configs.
- `OPERATOR`: View logs, manage users (limited).
- `VIEWER`: Read-only access.
- `USER`: Access to their own subscription page.

### Permission Mapping
- `users.*`: `[read, create, update, delete]`
- `servers.*`: `[read, create, update, delete]`
- `configs.*`: `[read, create, delete]`
- `security.*`: `[read, manage]`

## 3. Secret Management
- **Zero-Leak Policy:** Private keys are never logged, sent in API error responses, or committed to Git.
- **Storage:** Secrets stored in PostgreSQL encrypted at rest or handled as environment variables.
- **Environment:** Use `.env` files (ignored by Git) and Railway Secret variables.

## 4. API Security
- **Rate Limiting:** 
  - Login: 5 attempts per 15 mins per IP.
  - Public Subscriptions: 100 requests per hour per token.
- **Input Validation:** Strict Pydantic schemas for all API endpoints.
- **CORS:** Restricted to the frontend domain.

## 5. Audit Logging
Every administrative action is logged with:
- Timestamp
- Admin ID
- Action (e.g., `USER_DELETE`)
- Target ID
- IP Address
- Result (Success/Fail)
