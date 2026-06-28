import { useEffect, useState } from "react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { SelectField } from "@/components/ui/SelectField";
import type { PurchaseOrder, PurchaseReceiptCreateInput, Warehouse } from "@/types/api";

interface ReceiveGoodsModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: PurchaseReceiptCreateInput) => void;
  submitting: boolean;
  order: PurchaseOrder | null;
  warehouseOptions: { value: string; label: string }[];
  productNameById: Map<string, string>;
}

export function ReceiveGoodsModal({
  open,
  onClose,
  onSubmit,
  submitting,
  order,
  warehouseOptions,
  productNameById,
}: ReceiveGoodsModalProps) {
  const [warehouseId, setWarehouseId] = useState("");
  const [quantities, setQuantities] = useState<Record<string, number>>({});

  useEffect(() => {
    if (open && order) {
      setWarehouseId(warehouseOptions[0]?.value ?? "");
      const initial: Record<string, number> = {};
      for (const item of order.items) {
        initial[item.product_id] = Math.max(item.quantity - item.received_quantity, 0);
      }
      setQuantities(initial);
    }
  }, [open, order, warehouseOptions]);

  if (!order) return null;

  const currentOrder = order;
  const pendingItems = currentOrder.items.filter((item) => item.received_quantity < item.quantity);

  function handleSubmit() {
    const items = pendingItems
      .map((item) => ({
        product_id: item.product_id,
        quantity: Number(quantities[item.product_id] ?? 0),
        unit_cost: item.unit_cost,
      }))
      .filter((item) => item.quantity > 0);

    if (items.length === 0 || !warehouseId) return;

    onSubmit({ order_id: currentOrder.id, warehouse_id: warehouseId, items });
  }

  return (
    <Modal open={open} onClose={onClose} title={`استلام بضاعة - ${order.order_number}`} width={600}>
      <SelectField
        label="المخزن المستلم"
        required
        options={warehouseOptions}
        placeholder="اختر المخزن"
        value={warehouseId}
        onChange={(e) => setWarehouseId(e.target.value)}
      />

      <div style={{ marginTop: "var(--space-3)" }}>
        {pendingItems.length === 0 ? (
          <p style={{ color: "var(--color-ink-soft)", fontSize: "var(--text-sm)" }}>
            تم استلام جميع بنود هذا الطلب بالكامل.
          </p>
        ) : (
          <table className="data-table" style={{ width: "100%" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "right" }}>المنتج</th>
                <th style={{ textAlign: "center" }}>المتبقي</th>
                <th style={{ textAlign: "center" }}>الكمية المستلمة الآن</th>
              </tr>
            </thead>
            <tbody>
              {pendingItems.map((item) => {
                const remaining = item.quantity - item.received_quantity;
                return (
                  <tr key={item.id}>
                    <td>{productNameById.get(item.product_id) ?? item.product_id}</td>
                    <td className="numeric" style={{ textAlign: "center" }}>
                      {remaining}
                    </td>
                    <td style={{ textAlign: "center" }}>
                      <input
                        type="number"
                        className="field__input ltr-field"
                        style={{ width: 100, textAlign: "center" }}
                        min={0}
                        max={remaining}
                        step="0.001"
                        value={quantities[item.product_id] ?? 0}
                        onChange={(e) =>
                          setQuantities((prev) => ({ ...prev, [item.product_id]: Number(e.target.value) }))
                        }
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end", marginTop: "var(--space-5)" }}>
        <Button type="button" variant="ghost" onClick={onClose} disabled={submitting}>
          إلغاء
        </Button>
        <Button
          type="button"
          onClick={handleSubmit}
          loading={submitting}
          disabled={pendingItems.length === 0 || !warehouseId}
        >
          تأكيد الاستلام
        </Button>
      </div>
    </Modal>
  );
}
