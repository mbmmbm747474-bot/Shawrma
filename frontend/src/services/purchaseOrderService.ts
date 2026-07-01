import { api } from "@/services/apiClient";
import type {
  PurchaseOrder,
  PurchaseOrderCreateInput,
  PurchaseOrderUpdateInput,
} from "@/types/api";

export async function listPurchaseOrders(params?: {
  status?: string;
  supplierId?: string;
  branchId?: string;
}): Promise<PurchaseOrder[]> {
  const res = await api.get<PurchaseOrder[]>("/purchase-orders/", {
    params: {
      status_filter: params?.status,
      supplier_id: params?.supplierId,
      branch_id: params?.branchId,
    },
  });
  return res.data;
}

export async function getPurchaseOrder(id: string): Promise<PurchaseOrder> {
  const res = await api.get<PurchaseOrder>(`/purchase-orders/${id}`);
  return res.data;
}

export async function createPurchaseOrder(input: PurchaseOrderCreateInput): Promise<PurchaseOrder> {
  const res = await api.post<PurchaseOrder>("/purchase-orders/", input);
  return res.data;
}

export async function updatePurchaseOrder(
  id: string,
  input: PurchaseOrderUpdateInput,
): Promise<PurchaseOrder> {
  const res = await api.put<PurchaseOrder>(`/purchase-orders/${id}`, input);
  return res.data;
}

export async function approvePurchaseOrder(id: string): Promise<PurchaseOrder> {
  const res = await api.post<PurchaseOrder>(`/purchase-orders/${id}/approve`);
  return res.data;
}

export async function cancelPurchaseOrder(id: string): Promise<PurchaseOrder> {
  const res = await api.post<PurchaseOrder>(`/purchase-orders/${id}/cancel`);
  return res.data;
}

export async function deletePurchaseOrder(id: string): Promise<void> {
  await api.delete(`/purchase-orders/${id}`);
}
