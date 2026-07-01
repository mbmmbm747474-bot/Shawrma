import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, Warehouse as WarehouseIcon } from "lucide-react";
import { listWarehouses, createWarehouse, updateWarehouse, deleteWarehouse } from "@/services/warehouseService";
import { listBranches } from "@/services/branchService";
import type { Warehouse, WarehouseCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { WarehouseFormModal } from "./WarehouseFormModal";

export function WarehousesPage() {
  const queryClient = useQueryClient();
  const [editTarget, setEditTarget] = useState<Warehouse | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Warehouse | null>(null);

  const { data: warehouses, isLoading } = useQuery({ queryKey: ["warehouses"], queryFn: () => listWarehouses() });
  const { data: branches } = useQuery({ queryKey: ["branches"], queryFn: () => listBranches() });

  const branchNameById = useMemo(() => {
    const map = new Map<string, string>();
    branches?.forEach((b) => map.set(b.id, b.name));
    return map;
  }, [branches]);

  const createMutation = useMutation({
    mutationFn: (input: WarehouseCreateInput) => createWarehouse(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["warehouses"] });
      toast.success("تم إنشاء المخزن بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء المخزن")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: WarehouseCreateInput }) => {
      const { branch_id, ...rest } = input;
      return updateWarehouse(id, rest);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["warehouses"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteWarehouse(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["warehouses"] });
      toast.success("تم حذف المخزن");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف المخزن")),
  });

  const branchOptions = (branches ?? []).map((b) => ({ value: b.id, label: b.name }));

  const columns: Column<Warehouse>[] = [
    { header: "المخزن", accessor: (w) => <span style={{ fontWeight: 600 }}>{w.name}</span> },
    { header: "الفرع", accessor: (w) => branchNameById.get(w.branch_id) ?? "—" },
    { header: "الحالة", accessor: (w) => <StatusBadge active={w.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (w) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(w)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(w)}>
            <Trash2 size={15} />
          </IconButton>
        </div>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <CardHeader
          title="المخازن"
          subtitle="إدارة مخازن كل فرع"
          actions={
            <Button onClick={() => setCreateOpen(true)} disabled={branchOptions.length === 0}>
              <Plus size={16} />
              مخزن جديد
            </Button>
          }
        />

        {branchOptions.length === 0 && (
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
            أضف فرعًا أولًا قبل إنشاء المخازن.
          </div>
        )}

        {isLoading ? (
          <PageSpinner />
        ) : !warehouses || warehouses.length === 0 ? (
          <EmptyState icon={<WarehouseIcon size={32} />} title="لا توجد مخازن بعد" />
        ) : (
          <DataTable columns={columns} rows={warehouses} rowKey={(w) => w.id} />
        )}
      </Card>

      <WarehouseFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="مخزن جديد"
        branchOptions={branchOptions}
      />

      <WarehouseFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل المخزن"
        initialValues={editTarget ?? undefined}
        branchOptions={branchOptions}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف المخزن"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
