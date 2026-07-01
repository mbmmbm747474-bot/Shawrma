import { api } from "@/services/apiClient";
import type { PurchaseReceipt, PurchaseReceiptCreateInput } from "@/types/api";

export async function listReceipts(orderId?: string): Promise<PurchaseReceipt[]> {
  const res = await api.get<PurchaseReceipt[]>("/purchase-receipts/", {
    params: orderId ? { order_id: orderId } : undefined,
  });
  return res.data;
}

export async function createReceipt(input: PurchaseReceiptCreateInput): Promise<PurchaseReceipt> {
  const res = await api.post<PurchaseReceipt>("/purchase-receipts/", input);
  return res.data;
}
