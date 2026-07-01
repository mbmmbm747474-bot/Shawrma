from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.company import Company
from app.models.branch import Branch
from app.models.user import User
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.customer import Customer
from app.models.purchase_order import PurchaseOrder
from app.models.sales_invoice import SalesInvoice
from app.schemas.dashboard import DashboardSummary

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    company_id = current_user.company_id

    companies_count = db.query(Company).filter(Company.is_deleted == False).count()
    branches_count = (
        db.query(Branch)
        .filter(Branch.company_id == company_id, Branch.is_deleted == False)
        .count()
    )
    users_count = (
        db.query(User)
        .filter(User.company_id == company_id, User.is_deleted == False)
        .count()
    )
    products_count = (
        db.query(Product)
        .filter(Product.company_id == company_id, Product.is_deleted == False)
        .count()
    )
    suppliers_count = (
        db.query(Supplier)
        .filter(Supplier.company_id == company_id, Supplier.is_deleted == False)
        .count()
    )
    customers_count = (
        db.query(Customer)
        .filter(Customer.is_deleted == False)
        .count()
    )
    open_purchase_orders = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.status.in_(["DRAFT", "APPROVED"]),
            PurchaseOrder.is_deleted == False,
        )
        .count()
    )
    unpaid_sales_invoices = (
        db.query(SalesInvoice)
        .filter(
            SalesInvoice.status != "PAID",
            SalesInvoice.is_deleted == False,
        )
        .count()
    )

    return DashboardSummary(
        companies_count=companies_count,
        branches_count=branches_count,
        users_count=users_count,
        products_count=products_count,
        suppliers_count=suppliers_count,
        customers_count=customers_count,
        open_purchase_orders=open_purchase_orders,
        unpaid_sales_invoices=unpaid_sales_invoices,
    )
