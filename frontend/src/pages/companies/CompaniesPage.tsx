import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2 } from "lucide-react";
import { listCompanies, createCompany, updateCompany, deleteCompany } from "@/services/companyService";
import type { Company, CompanyCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { SearchInput } from "@/components/ui/SearchInput";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { Building2 } from "lucide-react";
import { CompanyFormModal } from "./CompanyFormModal";

export function CompaniesPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [editTarget, setEditTarget] = useState<Company | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Company | null>(null);

  const { data, isLoading } = useQuery({ queryKey: ["companies"], queryFn: listCompanies });

  const createMutation = useMutation({
    mutationFn: (input: CompanyCreateInput) => createCompany(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
      toast.success("تم إنشاء الشركة بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء الشركة")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: CompanyCreateInput }) => updateCompany(id, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteCompany(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["companies"] });
      toast.success("تم حذف الشركة");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف الشركة")),
  });

  const filtered = useMemo(() => {
    if (!data) return [];
    const q = search.trim().toLowerCase();
    if (!q) return data;
    return data.filter(
      (c) => c.name.toLowerCase().includes(q) || c.tax_number?.toLowerCase().includes(q),
    );
  }, [data, search]);

  const columns: Column<Company>[] = [
    {
      header: "الاسم",
      accessor: (c) => (
        <div>
          <div style={{ fontWeight: 600 }}>{c.name}</div>
          {c.legal_name && (
            <div style={{ fontSize: "var(--text-xs)", color: "var(--color-ink-soft)" }}>{c.legal_name}</div>
          )}
        </div>
      ),
    },
    { header: "الرقم الضريبي", accessor: (c) => <span className="ltr-field">{c.tax_number ?? "—"}</span> },
    { header: "العملة", accessor: (c) => <span className="ltr-field">{c.currency}</span> },
    { header: "الهاتف", accessor: (c) => <span className="ltr-field">{c.phone ?? "—"}</span> },
    { header: "الحالة", accessor: (c) => <StatusBadge active={c.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (c) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(c)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(c)}>
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
          title="الشركات"
          subtitle="إدارة الشركات المسجلة في النظام"
          actions={
            <Button onClick={() => setCreateOpen(true)}>
              <Plus size={16} />
              شركة جديدة
            </Button>
          }
        />

        <div style={{ marginBottom: "var(--space-4)" }}>
          <SearchInput value={search} onChange={setSearch} placeholder="بحث بالاسم أو الرقم الضريبي..." />
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={<Building2 size={32} />}
            title={search ? "لا توجد نتائج مطابقة" : "لا توجد شركات بعد"}
            description={search ? undefined : "أضف أول شركة للبدء في استخدام النظام."}
            action={
              !search && (
                <Button onClick={() => setCreateOpen(true)}>
                  <Plus size={16} />
                  إضافة شركة
                </Button>
              )
            }
          />
        ) : (
          <DataTable columns={columns} rows={filtered} rowKey={(c) => c.id} />
        )}
      </Card>

      <CompanyFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="شركة جديدة"
      />

      <CompanyFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل الشركة"
        initialValues={editTarget ?? undefined}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف الشركة"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟ لا يمكن التراجع عن هذا الإجراء.`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
