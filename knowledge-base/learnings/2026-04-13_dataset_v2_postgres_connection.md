# Dataset V2 Postgres Connection — Learnings

**Date**: 2026-04-13
**Context**: PLA-3416 — Cash flow fix invoices insertion into V2 infrastructure
**Author**: Thiago Rodrigues
**Related**: PLA-3376 (dataset migration), PLA-3417 (Retool migration)

---

## V2 Infrastructure Overview

The QuickBooks dataset was migrated from the legacy monolithic Postgres to the new V2 partitioned infrastructure. Each integration now has its **own dedicated database** on a shared Postgres cluster.

### Connection Details

| Field | Value |
|-------|-------|
| Host | `tbx-postgres-v2-unstable.flycast` |
| Port | `5432` |
| User | `postgres` |
| Database | `quickbooks` (NOT `postgres` — see gotcha below) |
| SSL | `disable` (internal flycast network) |
| Credentials | Bitwarden: "Dataset V2 Unstable Credentials" |
| Credentials (canonical) | AWS Parameter Store: `dataset-v2/unstable/postgres-connection-string` |

### Legacy vs V2

| | Legacy | V2 |
|---|--------|-----|
| Host | `tbx-postgres-staging.internal` | `tbx-postgres-v2-unstable.flycast` |
| Port | `5433` | `5432` |
| Database | `unstable` (monolithic) | `quickbooks` (per-integration) |
| User | `dataset` | `postgres` |
| Network | Tailscale VPN | `.flycast` private network (also via Tailscale) |

### Available Databases on V2 Instance

`archer`, `brevo`, `common`, `gem`, `gong`, `postgres`, `quickbooks`, `repmgr`, `siteimprove`, `tropic`

## Critical Gotchas

### 1. Default database is `postgres`, NOT your integration DB

When connecting for the first time, tools default to the `postgres` database. You **must** explicitly set `dbname=quickbooks` (or your integration name). If you insert into `postgres`, your data goes to the wrong place.

> Feedback from Diego Cavalli (via Lucas Scheffel): "Tem que cuidar que na hora de configurar o banco tu tem que selecionar o Database, normalmente o pessoal coloca o postgres ali. Nao tem como mudar isso dentro de um editor de SQL."

### 2. Unstable and Staging share the same V2 Postgres server

Per Coda docs, the unstable and staging environments use the same V2 Postgres instance. Different environments are separated by database name, not by host.

### 3. NOT NULL constraints differ from legacy

V2 schema has stricter NOT NULL constraints than legacy. Columns like `note_to_customer` on `quickbooks_invoices` are NOT NULL — empty strings (`''`) must be used instead of NULL.

### 4. Bitwarden entry naming

The canonical entry is: **"Dataset V2 Unstable Credentials"** (created by platform team). If you can't find it, check:
- Your collection/folder access (it's in a shared folder)
- Ask Lucas Scheffel or platform team for a Bitwarden Send link
- Fallback: AWS Parameter Store `dataset-v2/unstable/postgres-connection-string` (needs AWS access)

### 5. Hasura GraphQL layer

V2 also exposes data via Hasura: `https://tbx-hasura-v2-unstable.fly.dev`. This is what the ingestion pipeline and Retool use. Direct Postgres is for data insertion/debugging.

## Coda Documentation

The canonical V2 setup guide is in the Developers Coda doc:
- Doc: `https://coda.io/d/_dUwAsQie1Nk/`
- Page: "Creating a New Dataset" (canvas-Xx83ppbHHe) — has connection instructions
- Page: "Dataset V2 & DRM" (canvas-JiBst7n2WB) — architecture overview

## Activity Plans (Post-Insert)

After inserting data into V2, activity plans must be generated for the ingestion pipeline to pick up the rows and create them in QBO. This is a **platform team responsibility** (Augusto Gunsch). TSAs insert data; platform generates plans.

## Python Connection Snippet

```python
import psycopg2

conn = psycopg2.connect(
    host="tbx-postgres-v2-unstable.flycast",
    port=5432,
    user="postgres",
    password="<from Bitwarden>",
    dbname="quickbooks",  # IMPORTANT: not 'postgres'
    connect_timeout=15,
    sslmode="disable",
)
```

## Validation Checklist (Post-Insert)

1. Verify row counts match expected
2. Check FK integrity (no orphan line items)
3. Verify dataset_id matches target dataset
4. Check company_type distribution
5. Confirm no ID range conflicts with existing data
