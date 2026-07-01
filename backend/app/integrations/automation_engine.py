from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.sales_invoice import SalesInvoice
from app.models.inventory_stock_movement import InventoryStockMovement
from app.models.journal_entry import JournalEntry
from app.models.journal_item import JournalItem


class AutomationEngine:

    def process_sales_invoice(self, db: Session, invoice: SalesInvoice):

        if invoice.is_posted:
            return

        self._create_inventory_movements(db, invoice)
        self._create_journal_entry(db, invoice)

        invoice.is_posted = True
        db.add(invoice)

    # ---------------------------
    # INVENTORY AUTOMATION
    # ---------------------------
    def _create_inventory_movements(self, db: Session, invoice: SalesInvoice):

        for item in invoice.items:

            movement = InventoryStockMovement(
                product_id=item.product_id,
                warehouse_id=self._get_default_warehouse(db),
                movement_type="OUT",
                quantity=item.quantity,
                unit_cost=item.cost_price,
                reference_type="SALES",
                reference_id=invoice.id,
            )

            db.add(movement)

    # ---------------------------
    # ACCOUNTING AUTOMATION
    # ---------------------------
    def _create_journal_entry(self, db: Session, invoice: SalesInvoice):

        entry = JournalEntry(
            entry_number=f"JE-{invoice.invoice_number}",
            source_type="SALES",
            source_id=invoice.id,
            branch_id=invoice.branch_id,
            description="Auto posted sales invoice",
        )

        db.add(entry)
        db.flush()

        # Debit Cash / Receivable
        db.add(
            JournalItem(
                entry_id=entry.id,
                account_id=self._get_cash_account(db),
                debit=invoice.total,
                credit=0,
            )
        )

        # Credit Sales
        db.add(
            JournalItem(
                entry_id=entry.id,
                account_id=self._get_sales_account(db),
                debit=0,
                credit=invoice.total,
            )
        )

        # COGS (if inventory enabled)
        db.add(
            JournalItem(
                entry_id=entry.id,
                account_id=self._get_cogs_account(db),
                debit=self._calculate_cogs(invoice),
                credit=0,
            )
        )

        # Inventory reduction
        db.add(
            JournalItem(
                entry_id=entry.id,
                account_id=self._get_inventory_account(db),
                debit=0,
                credit=self._calculate_cogs(invoice),
            )
        )

    # ---------------------------
    # HELPERS
    # ---------------------------
    def _calculate_cogs(self, invoice):
        return sum(item.cost_price * item.quantity for item in invoice.items)

    def _get_default_warehouse(self, db): return 1
    def _get_cash_account(self, db): return 1
    def _get_sales_account(self, db): return 2
    def _get_cogs_account(self, db): return 3
    def _get_inventory_account(self, db): return 4
