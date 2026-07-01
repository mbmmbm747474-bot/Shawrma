"""add warehouse_id to purchase_receipts

Revision ID: dfd3e2040f18
Revises: e7748afe991c
Create Date: 2026-06-28 00:00:00.000000

This was missing from the initial schema: there was no way to know which
warehouse received goods on a purchase receipt, which is required to post
the correct InventoryStockMovement / InventoryBalance update. Added as
NOT NULL since this project has no production data yet; if you've already
deployed Milestone 1 with real purchase receipts, back up first and
backfill warehouse_id manually before running this migration.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "dfd3e2040f18"
down_revision: Union[str, None] = "e7748afe991c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "purchase_receipts",
        sa.Column("warehouse_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_foreign_key(
        "fk_purchase_receipts_warehouse_id",
        "purchase_receipts",
        "warehouses",
        ["warehouse_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_purchase_receipts_warehouse_id", "purchase_receipts", type_="foreignkey")
    op.drop_column("purchase_receipts", "warehouse_id")
