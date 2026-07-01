from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from app.models.inventory_balance import InventoryBalance
    from app.models.inventory_stock_movement import InventoryStockMovement


class StockEngine:
    """Maintains InventoryBalance using weighted-average cost.

    available_quantity = quantity_on_hand - reserved_quantity is kept in
    sync on every movement; reserved_quantity isn't touched here since
    nothing reserves stock yet (that belongs to a future Sales/POS
    milestone -- holding a quantity before it ships).
    """

    def update_balance_from_movement(self, db: Session, movement: "InventoryStockMovement") -> "InventoryBalance":
        from app.models.inventory_balance import InventoryBalance

        balance = (
            db.query(InventoryBalance)
            .filter_by(product_id=movement.product_id, warehouse_id=movement.warehouse_id)
            .first()
        )

        if not balance:
            balance = InventoryBalance(
                product_id=movement.product_id,
                warehouse_id=movement.warehouse_id,
                quantity_on_hand=0,
                reserved_quantity=0,
                available_quantity=0,
                average_cost=0,
            )
            db.add(balance)
            db.flush()

        if movement.movement_type == "IN":
            self._increase(balance, movement)
        elif movement.movement_type == "OUT":
            self._decrease(balance, movement)

        balance.available_quantity = balance.quantity_on_hand - balance.reserved_quantity
        db.add(balance)
        return balance

    def _increase(self, balance: "InventoryBalance", movement: "InventoryStockMovement") -> None:
        total_cost = (balance.quantity_on_hand * balance.average_cost) + (
            movement.quantity * (movement.unit_cost or 0)
        )
        new_qty = balance.quantity_on_hand + movement.quantity

        balance.average_cost = total_cost / new_qty if new_qty else 0
        balance.quantity_on_hand = new_qty

    def _decrease(self, balance: "InventoryBalance", movement: "InventoryStockMovement") -> None:
        # average_cost is unaffected by an OUT movement under weighted-average
        # costing; only quantity_on_hand changes. We don't block over-issuing
        # here (no hard floor at 0) since returns/corrections are legitimate
        # reasons stock can be adjusted; calling code decides what's allowed.
        balance.quantity_on_hand -= movement.quantity
