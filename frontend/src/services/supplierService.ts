import { api } from "@/services/apiClient";
import type { Supplier, SupplierCreateInput, SupplierUpdateInput } from "@/types/api";

export async function listSuppliers(): Promise<Supplier[]> {
  const res = await api.get<Supplier[]>("/suppliers/");
  return res.data;
}

export async function createSupplier(input: SupplierCreateInput): Promise<Supplier> {
  const res = await api.post<Supplier>("/suppliers/", input);
  return res.data;
}

export async function updateSupplier(id: string, input: SupplierUpdateInput): Promise<Supplier> {
  const res = await api.put<Supplier>(`/suppliers/${id}`, input);
  return res.data;
}

export async function deleteSupplier(id: string): Promise<void> {
  await api.delete(`/suppliers/${id}`);
}
