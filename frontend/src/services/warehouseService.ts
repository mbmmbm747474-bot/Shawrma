import { api } from "@/services/apiClient";
import type { Warehouse, WarehouseCreateInput, WarehouseUpdateInput } from "@/types/api";

export async function listWarehouses(branchId?: string): Promise<Warehouse[]> {
  const res = await api.get<Warehouse[]>("/warehouses/", {
    params: branchId ? { branch_id: branchId } : undefined,
  });
  return res.data;
}

export async function createWarehouse(input: WarehouseCreateInput): Promise<Warehouse> {
  const res = await api.post<Warehouse>("/warehouses/", input);
  return res.data;
}

export async function updateWarehouse(id: string, input: WarehouseUpdateInput): Promise<Warehouse> {
  const res = await api.put<Warehouse>(`/warehouses/${id}`, input);
  return res.data;
}

export async function deleteWarehouse(id: string): Promise<void> {
  await api.delete(`/warehouses/${id}`);
}
