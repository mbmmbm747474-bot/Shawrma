# Shawrma-City
# Restaurant ERP Pro

Enterprise ERP & POS System for Restaurants

Version: 0.1.0

---

## Project Status (read this first)

This README describes the **full target vision** for the system. Most of it
is **not built yet** — building an ERP this size is a multi-milestone effort.

**Done (Milestone 1 — Foundation):**
- Backend boots with FastAPI + SQLAlchemy (sync) + PostgreSQL
- Data model for all 13 domains below (Core, Inventory, Purchasing, Sales,
  Recipes, Accounting) — 34 tables, one Alembic migration
- JWT auth (login / refresh), password hashing
- Full CRUD: Users, Companies, Branches, Roles & Permissions
- Basic dashboard summary endpoint
- `scripts/seed_superuser.py` to bootstrap the first company/branch/superuser
- Docker Compose for postgres + redis + backend + pgadmin

**Not built yet:**
- Frontend (no `frontend/` folder exists; the React stack below is the plan, not reality)
- Inventory/Purchasing/Sales/Recipes/Accounting business endpoints (models exist, CRUD doesn't)
- Automation engines wiring sales → inventory → accounting (stub code exists in `app/integrations/`, not connected to any endpoint)
- HR, CRM, Finance modules (not modeled or coded at all)
- Reports, POS hardware integration (barcode/printing), Celery workers

See the milestone plan in this conversation, or ask for an updated status —
this section should be kept current as each milestone lands.

---

## Overview

Restaurant ERP Pro is a complete Enterprise Resource Planning (ERP) and Point of Sale (POS) platform designed for restaurants, cafés, food courts, cloud kitchens and restaurant chains.

The system includes:

- POS
- Inventory
- Purchasing
- Recipe Management
- Food Cost
- Accounting
- Finance
- HR
- CRM
- Dashboard
- Reports

---

# Technology Stack

## Backend

- Python 3.13
- FastAPI
- SQLAlchemy 2.x
- Alembic
- Pydantic
- PostgreSQL
- Redis
- Celery

## Frontend

- React
- TypeScript
- Vite
- Material UI
- Redux Toolkit
- React Query

## Database

PostgreSQL 17

---

# Features

## Core

- Multi Company
- Multi Branch
- Multi Warehouse
- Multi User
- Multi Currency
- Multi Language

---

## Security

- JWT Authentication
- Refresh Token
- RBAC Permissions
- Audit Log
- Password Policies
- Session Management

---

## POS

- Sales
- Returns
- Discounts
- Coupons
- Kitchen Orders
- Barcode
- QR Code
- Thermal Printing

---

## Inventory

- Raw Materials
- Finished Products
- Transfers
- Stock Count
- Stock Adjustment
- Waste Management
- Expiry Tracking

---

## Purchasing

- Suppliers
- Purchase Orders
- Goods Receipt
- Purchase Invoice
- Purchase Return

---

## Recipes

- Recipes
- Recipe Cost
- Yield
- Waste
- Versioning

---

## Accounting

- Chart Of Accounts
- Journal Entries
- General Ledger
- Trial Balance
- Income Statement
- Balance Sheet
- Cash Flow

---

## Finance

- Cashboxes
- Banks
- Expenses
- Receipts
- Payments

---

## HR

- Employees
- Attendance
- Payroll
- Loans
- Bonuses
- Vacations

---

## CRM

- Customers
- Loyalty
- Coupons
- Feedback

---

# Project Structure

Restaurant-ERP-Pro/

backend/

frontend/

database/

deployment/

docs/

tests/

scripts/

---

# Backend Structure

backend/

app/

api/

core/

models/

schemas/

repositories/

services/

security/

middleware/

events/

workers/

tests/

---

# Frontend Structure

frontend/

src/

components/

layouts/

pages/

hooks/

services/

store/

theme/

types/

---

# Database Structure

database/

schema/

migrations/

functions/

views/

triggers/

seed/

indexes/

---

# Architecture

- Clean Architecture
- Repository Pattern
- Unit Of Work
- SOLID Principles
- Dependency Injection
- Event Driven
- REST API
- Domain Driven Design

---

# Accounting Rules

- Double Entry Accounting
- Automatic Journal Posting
- VAT Included Prices
- Weighted Average Cost
- Recipe Based Consumption

---

# Default Modules

1. Core
2. Security
3. Products
4. Recipes
5. Inventory
6. Purchasing
7. Sales
8. POS
9. Accounting
10. Finance
11. HR
12. CRM
13. Reports

---

# Development

```bash
git clone https://github.com/your-company/restaurant-erp-pro.git
cd restaurant-erp-pro
```

Copy the environment template and adjust if needed:

```bash
cp backend/.env.example backend/.env
```

Start postgres, redis, pgadmin, and the backend:

```bash
docker compose up -d postgres redis backend pgadmin
```

Run database migrations (first time, and after pulling any future migration):

```bash
docker compose exec backend alembic upgrade head
```

Create your first company, branch, and superuser (interactive prompt —
there is no other way to get the first account, since every "create"
endpoint requires being logged in already):

```bash
docker compose exec backend python -m scripts.seed_superuser
```

Backend API

```
http://localhost:8000
```

Swagger / interactive docs

```
http://localhost:8000/docs
```

pgAdmin (DB browser)

```
http://localhost:5050
```

The `frontend` service in `docker-compose.yml` is commented out — there is no
`frontend/` app yet. It will be re-enabled once that milestone lands.

## Running tests

Every model uses Postgres-specific column types (`UUID`, `JSONB`), so the
test suite needs a real Postgres database — SQLite cannot represent this
schema at all. Easiest way, using the same Postgres container as dev:

```bash
docker compose exec postgres createdb -U postgres restaurant_erp_test
docker compose exec backend pytest
```

Or point `TEST_DATABASE_URL` at any throwaway Postgres database. Tests
create and drop every table per test, so never point it at a database with
real data.

---

# License

Commercial License

Restaurant ERP Pro

© 2026 All Rights Reserved
