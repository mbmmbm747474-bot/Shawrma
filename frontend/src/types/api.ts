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
