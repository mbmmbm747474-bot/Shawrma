class RecipeEngine:

    def consume_from_sale(self, db, invoice):

        for item in invoice.items:

            recipe = self._get_recipe(db, item.product_id)
            if not recipe:
                continue

            for ri in recipe.items:

                db.add(
                    InventoryStockMovement(
                        product_id=ri.product_id,
                        warehouse_id=1,
                        movement_type="OUT",
                        quantity=ri.quantity * item.quantity,
                        reference_type="RECIPE_CONSUMPTION",
                        reference_id=invoice.id,
                    )
                )

    def _get_recipe(self, db, product_id):
        from app.models.recipe import Recipe
        return db.query(Recipe).filter_by(product_id=product_id).first()
