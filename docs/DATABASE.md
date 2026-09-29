# Database Specification

## 1. Primary Store: PostgreSQL
PostgreSQL is used for all persistent data to ensure ACID compliance and scalability.

## 2. Schema Design

### `users` Table
- `id` (UUID, PK)
- `username` (String, Unique)
- `password_hash` (String)
- `email` (String, Unique)
- `role` (Enum: SUPER_ADMIN, ADMIN, etc.)
- `is_active` (Boolean)
- `two_fa_secret` (String, Encrypted)
- `created_at` (Timestamp)

### `servers` Table
- `id` (UUID, PK)
- `label` (String)
- `endpoint` (String)
- `port` (Integer)
- `location` (String)
- `protocol_supported` (Array/JSON)
- `status` (Enum: ONLINE, OFFLINE, DEGRADED)
- `last_seen` (Timestamp)

### `subscriptions` Table
- `id` (UUID, PK)
- `user_id` (FK -> users.id)
- `token` (String, Unique, Index)
- `traffic_limit` (BigInt) - bytes
- `traffic_used` (BigInt) - bytes
- `expiration_date` (Timestamp)
- `device_limit` (Integer)
- `status` (Enum: ACTIVE, EXPIRED, DISABLED)

### `configurations` Table
- `id` (UUID, PK)
- `sub_id` (FK -> subscriptions.id)
- `server_id` (FK -> servers.id)
- `protocol` (String)
- `config_data` (JSONB) - Stores protocol-specific params
- `link` (Text) - The generated URI
- `created_at` (Timestamp)

### `devices` Table
- `id` (UUID, PK)
- `sub_id` (FK -> subscriptions.id)
- `device_identifier` (String)
- `last_seen` (Timestamp)
- `ip_address` (String)

### `audit_logs` Table
- `id` (UUID, PK)
- `admin_id` (FK -> users.id)
- `action` (String)
- `target_id` (UUID)
- `timestamp` (Timestamp)
- `ip_address` (String)

## 3. Migrations
- Managed via **Alembic**.
- All changes must be scripted in `migrations/` directory.
