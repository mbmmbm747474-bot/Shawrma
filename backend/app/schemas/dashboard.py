from pydantic import BaseModel


class DashboardSummary(BaseModel):
    companies_count: int
    branches_count: int
    users_count: int
    products_count: int
    suppliers_count: int
    customers_count: int
    open_purchase_orders: int
    unpaid_sales_invoices: int
