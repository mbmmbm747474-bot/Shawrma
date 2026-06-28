// Mirrors backend/app/schemas/*.py exactly. Keep in sync with the backend
// schemas — these are not generated automatically in Milestone 1.

export interface Company {
  id: string;
  name: string;
  legal_name: string | null;
  tax_number: string | null;
  commercial_register: string | null;
  address: string | null;
  phone: string | null;
  email: string | null;
  currency: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CompanyCreateInput {
  name: string;
  legal_name?: string | null;
  tax_number?: string | null;
  commercial_register?: string | null;
  address?: string | null;
  phone?: string | null;
  email?: string | null;
  currency?: string;
  is_active?: boolean;
}

export type CompanyUpdateInput = Partial<CompanyCreateInput>;

export interface Branch {
  id: string;
  company_id: string;
  name: string;
  code: string | null;
  address: string | null;
  phone: string | null;
  email: string | null;
  manager_name: string | null;
  tax_number: string | null;
  opening_time: string | null;
  closing_time: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface BranchCreateInput {
  company_id: string;
  name: string;
  code?: string | null;
  address?: string | null;
  phone?: string | null;
  email?: string | null;
  manager_name?: string | null;
  tax_number?: string | null;
  opening_time?: string | null;
  closing_time?: string | null;
  is_active?: boolean;
}

export type BranchUpdateInput = Partial<Omit<BranchCreateInput, "company_id">>;

export interface User {
  id: string;
  username: string;
  email: string;
  full_name: string;
  mobile: string | null;
  language: string;
  timezone: string;
  avatar: string | null;
  is_active: boolean;
  is_superuser: boolean;
  company_id: string;
  branch_id: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreateInput {
  username: string;
  email: string;
  full_name: string;
  password: string;
  company_id: string;
  branch_id: string;
  mobile?: string | null;
  language?: string;
  timezone?: string;
  avatar?: string | null;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface UserUpdateInput {
  username?: string;
  email?: string;
  full_name?: string;
  password?: string;
  mobile?: string | null;
  language?: string;
  timezone?: string;
  avatar?: string | null;
  is_active?: boolean;
}

export interface DashboardSummary {
  companies_count: number;
  branches_count: number;
  users_count: number;
  products_count: number;
  suppliers_count: number;
  customers_count: number;
  open_purchase_orders: number;
  unpaid_sales_invoices: number;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string | { msg: string; loc: (string | number)[] }[];
}

// ---- Inventory ------------------------------------------------------

export interface Warehouse {
  id: string;
  branch_id: string;
  name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface WarehouseCreateInput {
  branch_id: string;
  name: string;
  is_active?: boolean;
}

export type WarehouseUpdateInput = Partial<Omit<WarehouseCreateInput, "branch_id">>;

export interface ProductCategory {
  id: string;
  company_id: string;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCategoryCreateInput {
  company_id: string;
  name: string;
  description?: string | null;
  is_active?: boolean;
}

export type ProductCategoryUpdateInput = Partial<Omit<ProductCategoryCreateInput, "company_id">>;

export interface Product {
  id: string;
  category_id: string;
  company_id: string;
  name: string;
  sku: string | null;
  barcode: string | null;
  sale_price: number;
  cost_price: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCreateInput {
  category_id: string;
  company_id: string;
  name: string;
  sku?: string | null;
  barcode?: string | null;
  sale_price?: number;
  cost_price?: number;
  is_active?: boolean;
}

export type ProductUpdateInput = Partial<Omit<ProductCreateInput, "company_id">>;

export interface InventoryBalance {
  id: string;
  product_id: string;
  warehouse_id: string;
  quantity_on_hand: number;
  reserved_quantity: number;
  available_quantity: number;
  average_cost: number;
  updated_at: string;
}

export interface StockMovement {
  id: string;
  product_id: string;
  warehouse_id: string;
  movement_type: "IN" | "OUT";
  quantity: number;
  unit_cost: number | null;
  movement_date: string;
  reference_type: string | null;
  reference_id: string | null;
  notes: string | null;
}

export interface StockAdjustmentInput {
  product_id: string;
  warehouse_id: string;
  movement_type: "IN" | "OUT";
  quantity: number;
  unit_cost?: number | null;
  notes?: string | null;
}

// ---- Purchasing -------------------------------------------------------

export interface Supplier {
  id: string;
  company_id: string;
  name: string;
  phone: string | null;
  email: string | null;
  address: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SupplierCreateInput {
  company_id: string;
  name: string;
  phone?: string | null;
  email?: string | null;
  address?: string | null;
  is_active?: boolean;
}

export type SupplierUpdateInput = Partial<Omit<SupplierCreateInput, "company_id">>;

export type PurchaseOrderStatus = "DRAFT" | "APPROVED" | "RECEIVED" | "CANCELLED";

export interface PurchaseOrderItem {
  id: string;
  product_id: string;
  quantity: number;
  unit_cost: number;
  total: number;
  received_quantity: number;
  notes: string | null;
}

export interface PurchaseOrderItemInput {
  product_id: string;
  quantity: number;
  unit_cost: number;
  notes?: string | null;
}

export interface PurchaseOrder {
  id: string;
  order_number: string;
  order_date: string;
  supplier_id: string;
  branch_id: string;
  status: PurchaseOrderStatus;
  subtotal: number;
  discount: number;
  tax: number;
  total: number;
  is_posted: boolean;
  items: PurchaseOrderItem[];
  created_at: string;
  updated_at: string;
}

export interface PurchaseOrderCreateInput {
  supplier_id: string;
  branch_id: string;
  discount?: number;
  tax?: number;
  items: PurchaseOrderItemInput[];
}

export interface PurchaseOrderUpdateInput {
  supplier_id?: string;
  discount?: number;
  tax?: number;
  items?: PurchaseOrderItemInput[];
}

export interface PurchaseReceiptItem {
  id: string;
  product_id: string;
  quantity: number;
  unit_cost: number;
  total: number;
}

export interface PurchaseReceiptItemInput {
  product_id: string;
  quantity: number;
  unit_cost: number;
}

export interface PurchaseReceipt {
  id: string;
  receipt_number: string;
  receipt_date: string;
  order_id: string;
  supplier_id: string;
  branch_id: string;
  warehouse_id: string;
  total: number;
  is_posted: boolean;
  items: PurchaseReceiptItem[];
  created_at: string;
}

export interface PurchaseReceiptCreateInput {
  order_id: string;
  warehouse_id: string;
  items: PurchaseReceiptItemInput[];
}
