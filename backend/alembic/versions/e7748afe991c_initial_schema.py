"""initial schema - foundation, inventory, purchasing, sales, recipes, accounting

Revision ID: e7748afe991c
Revises:
Create Date: 2026-06-27 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e7748afe991c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _audit_columns():
    """created_at/updated_at/created_by/updated_by/is_deleted/deleted_at/deleted_by
    used by every ERPBaseModel table. created_by/updated_by/deleted_by FKs to
    users.id are added separately via ALTER TABLE once `users` exists, to break
    the companies <-> users circular dependency."""
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tenant_id", sa.String(length=50), nullable=True),
    ]


def _simple_timestamps():
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


AUDIT_TABLES_NEEDING_USER_FK = [
    "companies",
    "customers",
    "product_categories",
    "products",
    "warehouses",
    "inventory_balances",
    "inventory_stock_movements",
    "suppliers",
    "supplier_payments",
    "purchase_orders",
    "purchase_order_items",
    "purchase_receipts",
    "purchase_receipt_items",
    "sales_invoices",
    "sales_invoice_items",
    "sales_payments",
    "recipes",
    "recipe_items",
    "recipe_cost_snapshots",
    "chart_of_accounts",
    "journal_entries",
    "journal_items",
    "accounting_settings",
]


def upgrade() -> None:
    # -------------------------------------------------------------------
    # Reference / lookup tables (no dependencies)
    # -------------------------------------------------------------------
    op.create_table(
        "languages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(10), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("is_rtl", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_simple_timestamps(),
    )

    op.create_table(
        "currencies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(10), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("symbol", sa.String(10), nullable=False),
        sa.Column("exchange_rate", sa.Numeric(18, 6), nullable=False, server_default="1"),
        sa.Column("is_base", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_simple_timestamps(),
    )

    op.create_table(
        "permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("module", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.UniqueConstraint("module", "action", name="uq_permissions_module_action"),
    )

    # -------------------------------------------------------------------
    # companies <-> users circular dependency:
    # create companies (audit FKs deferred), then users, then add FKs back.
    # -------------------------------------------------------------------
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("legal_name", sa.String(255), nullable=True),
        sa.Column("tax_number", sa.String(100), nullable=True),
        sa.Column("commercial_register", sa.String(100), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("currency", sa.String(10), nullable=False, server_default="EGP"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_audit_columns(),
    )
    op.create_index("ix_companies_name", "companies", ["name"])
    op.create_index("ix_companies_tax_number", "companies", ["tax_number"])

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("employee_no", sa.String(30), unique=True, nullable=True),
        sa.Column("username", sa.String(50), unique=True, nullable=False),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("mobile", sa.String(30), nullable=True),
        sa.Column("language", sa.String(10), nullable=False, server_default="ar"),
        sa.Column("timezone", sa.String(50), nullable=False, server_default="Africa/Cairo"),
        sa.Column("avatar", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("must_change_password", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), nullable=False),  # FK added after branches exists
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tenant_id", sa.String(length=50), nullable=True),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_branch_id", "users", ["branch_id"])

    # self-referential audit FKs on users
    op.create_foreign_key("fk_users_created_by", "users", "users", ["created_by"], ["id"])
    op.create_foreign_key("fk_users_updated_by", "users", "users", ["updated_by"], ["id"])
    op.create_foreign_key("fk_users_deleted_by", "users", "users", ["deleted_by"], ["id"])

    # -------------------------------------------------------------------
    # branches (depends on companies; users depends on branches)
    # -------------------------------------------------------------------
    op.create_table(
        "branches",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("code", sa.String(50), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("email", sa.String(200), nullable=True),
        sa.Column("manager_name", sa.String(200), nullable=True),
        sa.Column("tax_number", sa.String(100), nullable=True),
        sa.Column("opening_time", sa.Time(), nullable=True),
        sa.Column("closing_time", sa.Time(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # now that branches exists, wire up users.branch_id and companies audit FKs
    op.create_foreign_key("fk_users_branch_id", "users", "branches", ["branch_id"], ["id"])
    op.create_foreign_key("fk_companies_created_by", "companies", "users", ["created_by"], ["id"])
    op.create_foreign_key("fk_companies_updated_by", "companies", "users", ["updated_by"], ["id"])
    op.create_foreign_key("fk_companies_deleted_by", "companies", "users", ["deleted_by"], ["id"])

    # -------------------------------------------------------------------
    # Roles & permissions (depend on companies, users, branches, permissions)
    # -------------------------------------------------------------------
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_simple_timestamps(),
    )

    op.create_table(
        "role_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("permission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False),
        sa.UniqueConstraint("role_id", "permission_id", name="uq_role_permissions_role_permission"),
    )

    op.create_table(
        "user_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("roles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=True),
        sa.UniqueConstraint("user_id", "role_id", "branch_id", name="uq_user_roles_user_role_branch"),
    )

    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("refresh_token", sa.Text(), unique=True, nullable=False),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    op.create_table(
        "cost_centers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("code", sa.String(50), nullable=True),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("cost_centers.id"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_simple_timestamps(),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=True),
        sa.Column("table_name", sa.String(100), nullable=False),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("old_data", postgresql.JSONB(), nullable=True),
        sa.Column("new_data", postgresql.JSONB(), nullable=True),
        sa.Column("ip_address", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # -------------------------------------------------------------------
    # Inventory
    # -------------------------------------------------------------------
    op.create_table(
        "warehouses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_warehouses_name", "warehouses", ["name"])

    op.create_table(
        "product_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_product_categories_name", "product_categories", ["name"])
    op.create_index("ix_product_categories_company_id", "product_categories", ["company_id"])

    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("sku", sa.String(100), unique=True, nullable=True),
        sa.Column("barcode", sa.String(100), nullable=True),
        sa.Column("sale_price", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("cost_price", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("product_categories.id"), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_products_name", "products", ["name"])
    op.create_index("ix_products_sku", "products", ["sku"])
    op.create_index("ix_products_category_id", "products", ["category_id"])

    op.create_table(
        "inventory_balances",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id"), nullable=False),
        sa.Column("quantity_on_hand", sa.Numeric(12, 3), nullable=False, server_default="0"),
        sa.Column("reserved_quantity", sa.Numeric(12, 3), nullable=False, server_default="0"),
        sa.Column("available_quantity", sa.Numeric(12, 3), nullable=False, server_default="0"),
        sa.Column("average_cost", sa.Numeric(12, 2), nullable=False, server_default="0"),
        *_audit_columns(),
    )
    op.create_index(
        "ix_inventory_balance_product_warehouse",
        "inventory_balances",
        ["product_id", "warehouse_id"],
        unique=True,
    )

    op.create_table(
        "inventory_stock_movements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("warehouses.id"), nullable=False),
        sa.Column("movement_type", sa.String(10), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("movement_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("reference_type", sa.String(50), nullable=True),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("notes", sa.String(255), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_stock_movements_product_id", "inventory_stock_movements", ["product_id"])
    op.create_index("ix_stock_movements_warehouse_id", "inventory_stock_movements", ["warehouse_id"])
    op.create_index(
        "ix_stock_movements_reference",
        "inventory_stock_movements",
        ["reference_type", "reference_id"],
    )

    # -------------------------------------------------------------------
    # Purchasing
    # -------------------------------------------------------------------
    op.create_table(
        "suppliers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_suppliers_name", "suppliers", ["name"])
    op.create_index("ix_suppliers_company_id", "suppliers", ["company_id"])

    op.create_table(
        "supplier_payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("supplier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("payment_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("method", sa.String(30), nullable=False, server_default="CASH"),
        sa.Column("reference", sa.String(100), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_supplier_payments_supplier_id", "supplier_payments", ["supplier_id"])

    op.create_table(
        "purchase_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_number", sa.String(50), unique=True, nullable=False),
        sa.Column("order_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("supplier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("tax", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("is_posted", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_audit_columns(),
    )
    op.create_index("ix_purchase_orders_number", "purchase_orders", ["order_number"])
    op.create_index("ix_purchase_orders_supplier_id", "purchase_orders", ["supplier_id"])
    op.create_index("ix_purchase_orders_branch_id", "purchase_orders", ["branch_id"])

    op.create_table(
        "purchase_order_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("purchase_orders.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        sa.Column("received_quantity", sa.Numeric(12, 3), nullable=False, server_default="0"),
        sa.Column("notes", sa.String(255), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_purchase_items_order_id", "purchase_order_items", ["order_id"])
    op.create_index("ix_purchase_items_product_id", "purchase_order_items", ["product_id"])

    op.create_table(
        "purchase_receipts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("receipt_number", sa.String(50), unique=True, nullable=False),
        sa.Column("receipt_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("purchase_orders.id"), nullable=False),
        sa.Column("supplier_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("suppliers.id"), nullable=False),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=False),
        sa.Column("total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("is_posted", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_audit_columns(),
    )
    op.create_index("ix_purchase_receipts_number", "purchase_receipts", ["receipt_number"])
    op.create_index("ix_purchase_receipts_order_id", "purchase_receipts", ["order_id"])

    op.create_table(
        "purchase_receipt_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("receipt_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("purchase_receipts.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_receipt_items_receipt_id", "purchase_receipt_items", ["receipt_id"])
    op.create_index("ix_receipt_items_product_id", "purchase_receipt_items", ["product_id"])

    # -------------------------------------------------------------------
    # Sales / POS
    # -------------------------------------------------------------------
    op.create_table(
        "customers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_audit_columns(),
    )
    op.create_index("ix_customers_name", "customers", ["name"])
    op.create_index("ix_customers_phone", "customers", ["phone"])

    op.create_table(
        "sales_invoices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("invoice_number", sa.String(50), unique=True, nullable=False),
        sa.Column("invoice_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("customers.id"), nullable=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("tax", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("paid_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("remaining_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("is_posted", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_audit_columns(),
    )
    op.create_index("ix_sales_invoices_number", "sales_invoices", ["invoice_number"])
    op.create_index("ix_sales_invoices_customer_id", "sales_invoices", ["customer_id"])
    op.create_index("ix_sales_invoices_branch_id", "sales_invoices", ["branch_id"])

    op.create_table(
        "sales_invoice_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sales_invoices.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("cost_price", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total", sa.Numeric(12, 2), nullable=False),
        sa.Column("notes", sa.String(255), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_sales_invoice_items_invoice_id", "sales_invoice_items", ["invoice_id"])
    op.create_index("ix_sales_invoice_items_product_id", "sales_invoice_items", ["product_id"])

    op.create_table(
        "sales_payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("invoice_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sales_invoices.id"), nullable=False),
        sa.Column("payment_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("method", sa.String(30), nullable=False, server_default="CASH"),
        sa.Column("reference", sa.String(100), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_sales_payments_invoice_id", "sales_payments", ["invoice_id"])

    # -------------------------------------------------------------------
    # Recipes
    # -------------------------------------------------------------------
    op.create_table(
        "recipes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), unique=True, nullable=False),
        sa.Column("yield_quantity", sa.Numeric(12, 3), nullable=False, server_default="1"),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_recipes_product_id", "recipes", ["product_id"])
    op.create_index("ix_recipes_company_id", "recipes", ["company_id"])

    op.create_table(
        "recipe_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("recipe_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("recipes.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Numeric(12, 3), nullable=False),
        sa.Column("unit_cost", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("unit", sa.String(20), nullable=True),
        *_audit_columns(),
    )
    op.create_index("ix_recipe_items_recipe_id", "recipe_items", ["recipe_id"])
    op.create_index("ix_recipe_items_product_id", "recipe_items", ["product_id"])

    op.create_table(
        "recipe_cost_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("recipe_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("recipes.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("cost_per_unit", sa.Numeric(12, 2), nullable=False),
        sa.Column("food_cost_percentage", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("snapshot_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        *_audit_columns(),
    )
    op.create_index("ix_recipe_snapshots_recipe_id", "recipe_cost_snapshots", ["recipe_id"])

    # -------------------------------------------------------------------
    # Accounting
    # -------------------------------------------------------------------
    op.create_table(
        "chart_of_accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("account_type", sa.String(20), nullable=False),
        sa.Column("is_postable", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chart_of_accounts.id"), nullable=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_accounts_code", "chart_of_accounts", ["code"])
    op.create_index("ix_accounts_parent_id", "chart_of_accounts", ["parent_id"])

    op.create_table(
        "journal_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entry_number", sa.String(50), unique=True, nullable=False),
        sa.Column("entry_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("is_posted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("source_type", sa.String(50), nullable=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("branch_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("branches.id"), nullable=False),
        *_audit_columns(),
    )
    op.create_index("ix_journal_entries_number", "journal_entries", ["entry_number"])
    op.create_index("ix_journal_entries_date", "journal_entries", ["entry_date"])

    op.create_table(
        "journal_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entry_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("journal_entries.id"), nullable=False),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chart_of_accounts.id"), nullable=False),
        sa.Column("description", sa.String(255), nullable=True),
        sa.Column("debit", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("credit", sa.Numeric(12, 2), nullable=False, server_default="0"),
        *_audit_columns(),
    )
    op.create_index("ix_journal_items_entry_id", "journal_items", ["entry_id"])
    op.create_index("ix_journal_items_account_id", "journal_items", ["account_id"])

    op.create_table(
        "accounting_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), unique=True, nullable=False),
        sa.Column("cash_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("sales_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("inventory_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("cost_of_goods_sold_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tax_account_id", postgresql.UUID(as_uuid=True), nullable=True),
        *_audit_columns(),
    )

    # -------------------------------------------------------------------
    # Add created_by/updated_by/deleted_by -> users.id FKs for every
    # ERPBaseModel table created above (now that `users` exists).
    # -------------------------------------------------------------------
    for table in AUDIT_TABLES_NEEDING_USER_FK:
        op.create_foreign_key(f"fk_{table}_created_by", table, "users", ["created_by"], ["id"])
        op.create_foreign_key(f"fk_{table}_updated_by", table, "users", ["updated_by"], ["id"])
        op.create_foreign_key(f"fk_{table}_deleted_by", table, "users", ["deleted_by"], ["id"])


def downgrade() -> None:
    op.drop_table("accounting_settings")
    op.drop_table("journal_items")
    op.drop_table("journal_entries")
    op.drop_table("chart_of_accounts")
    op.drop_table("recipe_cost_snapshots")
    op.drop_table("recipe_items")
    op.drop_table("recipes")
    op.drop_table("sales_payments")
    op.drop_table("sales_invoice_items")
    op.drop_table("sales_invoices")
    op.drop_table("customers")
    op.drop_table("purchase_receipt_items")
    op.drop_table("purchase_receipts")
    op.drop_table("purchase_order_items")
    op.drop_table("purchase_orders")
    op.drop_table("supplier_payments")
    op.drop_table("suppliers")
    op.drop_table("inventory_stock_movements")
    op.drop_table("inventory_balances")
    op.drop_table("products")
    op.drop_table("product_categories")
    op.drop_table("warehouses")
    op.drop_table("audit_logs")
    op.drop_table("cost_centers")
    op.drop_table("user_sessions")
    op.drop_table("user_roles")
    op.drop_table("role_permissions")
    op.drop_table("roles")
    op.drop_constraint("fk_companies_deleted_by", "companies", type_="foreignkey")
    op.drop_constraint("fk_companies_updated_by", "companies", type_="foreignkey")
    op.drop_constraint("fk_companies_created_by", "companies", type_="foreignkey")
    op.drop_constraint("fk_users_branch_id", "users", type_="foreignkey")
    op.drop_table("branches")
    op.drop_constraint("fk_users_deleted_by", "users", type_="foreignkey")
    op.drop_constraint("fk_users_updated_by", "users", type_="foreignkey")
    op.drop_constraint("fk_users_created_by", "users", type_="foreignkey")
    op.drop_table("users")
    op.drop_table("companies")
    op.drop_table("permissions")
    op.drop_table("currencies")
    op.drop_table("languages")
