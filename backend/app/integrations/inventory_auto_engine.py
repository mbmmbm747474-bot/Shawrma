class StockEngine:

    def update_balance_from_movement(self, db, movement):

        from app.models.inventory_balance import InventoryBalance

        balance = db.query(InventoryBalance).filter_by(
            product_id=movement.product_id,
            warehouse_id=movement.warehouse_id
        ).first()

        if not balance:
            balance = InventoryBalance(
                product_id=movement.product_id,
                warehouse_id=movement.warehouse_id,
                quantity_on_hand=0,
                average_cost=0,
            )
            db.add(balance)
            db.flush()

        if movement.movement_type == "IN":
            self._increase(balance, movement)

        elif movement.movement_type == "OUT":
            self._decrease(balance, movement)

    def _increase(self, balance, movement):
        total_cost = (balance.quantity_on_hand * balance.average_cost) + \
                     (movement.quantity * (movement.unit_cost or 0))

        new_qty = balance.quantity_on_hand + movement.quantity

        balance.average_cost = total_cost / new_qty if new_qty else 0
        balance.quantity_on_hand = new_qty

    def _decrease(self, balance, movement):
        balance.quantity_on_hand -= movement.quantity
