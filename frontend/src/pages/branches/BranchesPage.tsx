import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, GitBranch } from "lucide-react";
import { listBranches, createBranch, updateBranch, deleteBranch } from "@/services/branchService";
import { listCompanies } from "@/services/companyService";
import type { Branch, BranchCreateInput } from "@/types/api";
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
import { BranchFormModal } from "./BranchFormModal";

export function BranchesPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [editTarget, setEditTarget] = useState<Branch | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Branch | null>(null);

  const { data: branches, isLoading } = useQuery({ queryKey: ["branches"], queryFn: () => listBranches() });
  const { data: companies } = useQuery({ queryKey: ["companies"], queryFn: listCompanies });

  const companyNameById = useMemo(() => {
    const map = new Map<string, string>();
    companies?.forEach((c) => map.set(c.id, c.name));
    return map;
  }, [companies]);

  const createMutation = useMutation({
    mutationFn: (input: BranchCreateInput) => createBranch(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["branches"] });
      toast.success("تم إنشاء الفرع بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء الفرع")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: BranchCreateInput }) => {
      const { company_id, ...updatePayload } = input;
      return updateBranch(id, updatePayload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["branches"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteBranch(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["branches"] });
      toast.success("تم حذف الفرع");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف الفرع")),
  });

  const filtered = useMemo(() => {
    if (!branches) return [];
    const q = search.trim().toLowerCase();
    if (!q) return branches;
    return branches.filter(
      (b) => b.name.toLowerCase().includes(q) || (companyNameById.get(b.company_id) ?? "").toLowerCase().includes(q),
    );
  }, [branches, search, companyNameById]);

  const columns: Column<Branch>[] = [
    {
      header: "الفرع",
      accessor: (b) => (
        <div>
          <div style={{ fontWeight: 600 }}>{b.name}</div>
          {b.code && <div style={{ fontSize: "var(--text-xs)", color: "var(--color-ink-soft)" }} className="ltr-field">{b.code}</div>}
        </div>
      ),
    },
    { header: "الشركة", accessor: (b) => companyNameById.get(b.company_id) ?? "—" },
    { header: "المدير", accessor: (b) => b.manager_name ?? "—" },
    { header: "الهاتف", accessor: (b) => <span className="ltr-field">{b.phone ?? "—"}</span> },
    { header: "الحالة", accessor: (b) => <StatusBadge active={b.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (b) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(b)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(b)}>
            <Trash2 size={15} />
          </IconButton>
        </div>
      ),
    },
  ];

  const companyOptions = (companies ?? []).map((c) => ({ value: c.id, label: c.name }));

  return (
    <div>
      <Card>
        <CardHeader
          title="الفروع"
          subtitle="إدارة فروع الشركات"
          actions={
            <Button onClick={() => setCreateOpen(true)} disabled={companyOptions.length === 0}>
              <Plus size={16} />
              فرع جديد
            </Button>
          }
        />

        {companyOptions.length === 0 && (
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
            أضف شركة أولًا قبل إنشاء الفروع.
          </div>
        )}

        <div style={{ marginBottom: "var(--space-4)" }}>
          <SearchInput value={search} onChange={setSearch} placeholder="بحث بالاسم أو الشركة..." />
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState
            icon={<GitBranch size={32} />}
            title={search ? "لا توجد نتائج مطابقة" : "لا توجد فروع بعد"}
          />
        ) : (
          <DataTable columns={columns} rows={filtered} rowKey={(b) => b.id} />
        )}
      </Card>

      <BranchFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="فرع جديد"
        companyOptions={companyOptions}
      />

      <BranchFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل الفرع"
        initialValues={editTarget ?? undefined}
        companyOptions={companyOptions}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف الفرع"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟ لا يمكن التراجع عن هذا الإجراء.`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
