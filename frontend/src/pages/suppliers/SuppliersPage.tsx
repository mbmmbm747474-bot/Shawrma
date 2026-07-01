import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, Truck } from "lucide-react";
import { listSuppliers, createSupplier, updateSupplier, deleteSupplier } from "@/services/supplierService";
import type { Supplier, SupplierCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { useAuthStore } from "@/store/authStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { SearchInput } from "@/components/ui/SearchInput";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { SupplierFormModal } from "./SupplierFormModal";

export function SuppliersPage() {
  const queryClient = useQueryClient();
  const currentUser = useAuthStore((s) => s.user);
  const [search, setSearch] = useState("");
  const [editTarget, setEditTarget] = useState<Supplier | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Supplier | null>(null);

  const { data: suppliers, isLoading } = useQuery({ queryKey: ["suppliers"], queryFn: listSuppliers });

  const createMutation = useMutation({
    mutationFn: (input: SupplierCreateInput) => createSupplier(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["suppliers"] });
      toast.success("تم إنشاء المورد بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء المورد")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: SupplierCreateInput }) => {
      const { company_id, ...rest } = input;
      return updateSupplier(id, rest);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["suppliers"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteSupplier(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["suppliers"] });
      toast.success("تم حذف المورد");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف المورد")),
  });

  const filtered = useMemo(() => {
    if (!suppliers) return [];
    const q = search.trim().toLowerCase();
    if (!q) return suppliers;
    return suppliers.filter((s) => s.name.toLowerCase().includes(q));
  }, [suppliers, search]);

  const columns: Column<Supplier>[] = [
    { header: "المورد", accessor: (s) => <span style={{ fontWeight: 600 }}>{s.name}</span> },
    { header: "الهاتف", accessor: (s) => <span className="ltr-field">{s.phone ?? "—"}</span> },
    { header: "البريد الإلكتروني", accessor: (s) => <span className="ltr-field">{s.email ?? "—"}</span> },
    { header: "الحالة", accessor: (s) => <StatusBadge active={s.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (s) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(s)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(s)}>
            <Trash2 size={15} />
          </IconButton>
        </div>
      ),
    },
  ];

  if (!currentUser) return <PageSpinner />;

  return (
    <div>
      <Card>
        <CardHeader
          title="الموردون"
          subtitle="إدارة موردي الشركة"
          actions={
            <Button onClick={() => setCreateOpen(true)}>
              <Plus size={16} />
              مورد جديد
            </Button>
          }
        />

        <div style={{ marginBottom: "var(--space-4)" }}>
          <SearchInput value={search} onChange={setSearch} placeholder="بحث بالاسم..." />
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState icon={<Truck size={32} />} title={search ? "لا توجد نتائج مطابقة" : "لا يوجد موردون بعد"} />
        ) : (
          <DataTable columns={columns} rows={filtered} rowKey={(s) => s.id} />
        )}
      </Card>

      <SupplierFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="مورد جديد"
        companyId={currentUser.company_id}
      />

      <SupplierFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل المورد"
        initialValues={editTarget ?? undefined}
        companyId={currentUser.company_id}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف المورد"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
