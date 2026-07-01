from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    roles,
    permissions,
    companies,
    branches,
    dashboard,
    warehouses,
    product_categories,
    products,
    inventory,
    suppliers,
    purchase_orders,
    purchase_receipts,
)

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["Roles"],
)

api_router.include_router(
    permissions.router,
    prefix="/permissions",
    tags=["Permissions"],
)

api_router.include_router(
    companies.router,
    prefix="/companies",
    tags=["Companies"],
)

api_router.include_router(
    branches.router,
    prefix="/branches",
    tags=["Branches"],
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
)

api_router.include_router(
    warehouses.router,
    prefix="/warehouses",
    tags=["Warehouses"],
)

api_router.include_router(
    product_categories.router,
    prefix="/product-categories",
    tags=["Product Categories"],
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["Products"],
)

api_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"],
)

api_router.include_router(
    suppliers.router,
    prefix="/suppliers",
    tags=["Suppliers"],
)

api_router.include_router(
    purchase_orders.router,
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)

api_router.include_router(
    purchase_receipts.router,
    prefix="/purchase-receipts",
    tags=["Purchase Receipts"],
)
