import { api } from "@/services/apiClient";
import type { InventoryBalance, StockAdjustmentInput, StockMovement } from "@/types/api";

export async function listBalances(params?: {
  warehouseId?: string;
  productId?: string;
}): Promise<InventoryBalance[]> {
  const res = await api.get<InventoryBalance[]>("/inventory/balances", {
    params: {
      warehouse_id: params?.warehouseId,
      product_id: params?.productId,
    },
  });
  return res.data;
}

export async function listMovements(params?: {
  productId?: string;
  warehouseId?: string;
}): Promise<StockMovement[]> {
  const res = await api.get<StockMovement[]>("/inventory/movements", {
    params: {
      product_id: params?.productId,
      warehouse_id: params?.warehouseId,
    },
  });
  return res.data;
}

export async function createAdjustment(input: StockAdjustmentInput): Promise<StockMovement> {
  const res = await api.post<StockMovement>("/inventory/adjustments", input);
  return res.data;
}
