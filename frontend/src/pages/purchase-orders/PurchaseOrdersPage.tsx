import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, ClipboardList, Check, X, PackageCheck } from "lucide-react";
import {
  listPurchaseOrders,
  createPurchaseOrder,
  updatePurchaseOrder,
  approvePurchaseOrder,
  cancelPurchaseOrder,
  deletePurchaseOrder,
} from "@/services/purchaseOrderService";
import { createReceipt } from "@/services/purchaseReceiptService";
import { listSuppliers } from "@/services/supplierService";
import { listProducts } from "@/services/productService";
import { listBranches } from "@/services/branchService";
import { listWarehouses } from "@/services/warehouseService";
import type { PurchaseOrder, PurchaseOrderCreateInput, PurchaseOrderStatus, PurchaseReceiptCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { ToneBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { PurchaseOrderFormModal } from "./PurchaseOrderFormModal";
import { ReceiveGoodsModal } from "./ReceiveGoodsModal";

function formatMoney(value: number): string {
  return value.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const STATUS_LABELS: Record<PurchaseOrderStatus, string> = {
  DRAFT: "مسودة",
  APPROVED: "معتمد",
  RECEIVED: "مستلم",
  CANCELLED: "ملغي",
};

const STATUS_TONES: Record<PurchaseOrderStatus, "warning" | "info" | "active" | "danger"> = {
  DRAFT: "warning",
  APPROVED: "info",
  RECEIVED: "active",
  CANCELLED: "danger",
};

export function PurchaseOrdersPage() {
  const queryClient = useQueryClient();
  const [editTarget, setEditTarget] = useState<PurchaseOrder | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<PurchaseOrder | null>(null);
  const [receiveTarget, setReceiveTarget] = useState<PurchaseOrder | null>(null);

  const { data: orders, isLoading } = useQuery({ queryKey: ["purchase-orders"], queryFn: () => listPurchaseOrders() });
  const { data: suppliers } = useQuery({ queryKey: ["suppliers"], queryFn: listSuppliers });
  const { data: products } = useQuery({ queryKey: ["products"], queryFn: () => listProducts() });
  const { data: branches } = useQuery({ queryKey: ["branches"], queryFn: () => listBranches() });
  const { data: warehouses } = useQuery({ queryKey: ["warehouses"], queryFn: () => listWarehouses() });

  const supplierNameById = useMemo(() => {
    const map = new Map<string, string>();
    suppliers?.forEach((s) => map.set(s.id, s.name));
    return map;
  }, [suppliers]);

  const productNameById = useMemo(() => {
    const map = new Map<string, string>();
    products?.forEach((p) => map.set(p.id, p.name));
    return map;
  }, [products]);

  const invalidateOrders = () => {
    queryClient.invalidateQueries({ queryKey: ["purchase-orders"] });
    queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
  };

  const createMutation = useMutation({
    mutationFn: (input: PurchaseOrderCreateInput) => createPurchaseOrder(input),
    onSuccess: () => {
      invalidateOrders();
      toast.success("تم إنشاء أمر الشراء بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء أمر الشراء")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: PurchaseOrderCreateInput }) => {
      const { branch_id, ...rest } = input;
      return updatePurchaseOrder(id, rest);
    },
    onSuccess: () => {
      invalidateOrders();
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const approveMutation = useMutation({
    mutationFn: (id: string) => approvePurchaseOrder(id),
    onSuccess: () => {
      invalidateOrders();
      toast.success("تم اعتماد أمر الشراء");
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل اعتماد أمر الشراء")),
  });

  const cancelMutation = useMutation({
    mutationFn: (id: string) => cancelPurchaseOrder(id),
    onSuccess: () => {
      invalidateOrders();
      toast.success("تم إلغاء أمر الشراء");
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إلغاء أمر الشراء")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deletePurchaseOrder(id),
    onSuccess: () => {
      invalidateOrders();
      toast.success("تم حذف أمر الشراء");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف أمر الشراء")),
  });

  const receiveMutation = useMutation({
    mutationFn: (input: PurchaseReceiptCreateInput) => createReceipt(input),
    onSuccess: () => {
      invalidateOrders();
      queryClient.invalidateQueries({ queryKey: ["inventory-balances"] });
      toast.success("تم تسجيل استلام البضاعة وتحديث المخزون");
      setReceiveTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل تسجيل الاستلام")),
  });

  const columns: Column<PurchaseOrder>[] = [
    { header: "رقم الطلب", accessor: (o) => <span className="ltr-field" style={{ fontWeight: 600 }}>{o.order_number}</span> },
    { header: "المورد", accessor: (o) => supplierNameById.get(o.supplier_id) ?? "—" },
    { header: "الحالة", accessor: (o) => <ToneBadge tone={STATUS_TONES[o.status]}>{STATUS_LABELS[o.status]}</ToneBadge> },
    { header: "الإجمالي", align: "end", accessor: (o) => <span className="numeric">{formatMoney(o.total)}</span> },
    {
      header: "",
      align: "end",
      accessor: (o) => (
        <div className="row-actions">
          {o.status === "DRAFT" && (
            <>
              <IconButton aria-label="تعديل" onClick={() => setEditTarget(o)}>
                <Pencil size={15} />
              </IconButton>
              <IconButton aria-label="اعتماد" onClick={() => approveMutation.mutate(o.id)} title="اعتماد">
                <Check size={15} />
              </IconButton>
              <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(o)}>
                <Trash2 size={15} />
              </IconButton>
            </>
          )}
          {o.status === "APPROVED" && (
            <>
              <IconButton aria-label="استلام بضاعة" onClick={() => setReceiveTarget(o)} title="استلام بضاعة">
                <PackageCheck size={15} />
              </IconButton>
              <IconButton aria-label="إلغاء" variant="danger" onClick={() => cancelMutation.mutate(o.id)} title="إلغاء">
                <X size={15} />
              </IconButton>
            </>
          )}
        </div>
      ),
    },
  ];

  const branchOptions = (branches ?? []).map((b) => ({ value: b.id, label: b.name }));
  const warehouseOptions = (warehouses ?? []).map((w) => ({ value: w.id, label: w.name }));

  const canCreate = (suppliers?.length ?? 0) > 0 && (products?.length ?? 0) > 0 && branchOptions.length > 0;

  return (
    <div>
      <Card>
        <CardHeader
          title="أوامر الشراء"
          subtitle="إنشاء واعتماد واستلام أوامر الشراء من الموردين"
          actions={
            <Button onClick={() => setCreateOpen(true)} disabled={!canCreate}>
              <Plus size={16} />
              أمر شراء جديد
            </Button>
          }
        />

        {!canCreate && (
          <div
            style={{
              background: "var(--color-saffron-soft)",
              color: "var(--color-saffron-dark)",
              padding: "var(--space-3) var(--space-4)",
              borderRadius: "var(--radius-md)",
              fontSize: "var(--text-sm)",
              marginBottom: "var(--space-4)",
            }}
          >
            تحتاج إلى مورد واحد ومنتج واحد على الأقل وفرع لإنشاء أمر شراء.
          </div>
        )}

        {isLoading ? (
          <PageSpinner />
        ) : !orders || orders.length === 0 ? (
          <EmptyState icon={<ClipboardList size={32} />} title="لا توجد أوامر شراء بعد" />
        ) : (
          <DataTable columns={columns} rows={orders} rowKey={(o) => o.id} />
        )}
      </Card>

      <PurchaseOrderFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        suppliers={suppliers ?? []}
        products={products ?? []}
        branchOptions={branchOptions}
      />

      <PurchaseOrderFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        suppliers={suppliers ?? []}
        products={products ?? []}
        branchOptions={branchOptions}
        initialValues={editTarget ?? undefined}
      />

      <ReceiveGoodsModal
        open={Boolean(receiveTarget)}
        onClose={() => setReceiveTarget(null)}
        onSubmit={(values) => receiveMutation.mutate(values)}
        submitting={receiveMutation.isPending}
        order={receiveTarget}
        warehouseOptions={warehouseOptions}
        productNameById={productNameById}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف أمر الشراء"
        message={`هل أنت متأكد من حذف أمر الشراء "${deleteTarget?.order_number}"؟`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
