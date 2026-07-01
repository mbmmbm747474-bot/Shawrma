import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, Users as UsersIcon, ShieldCheck } from "lucide-react";
import { listUsers, createUser, updateUser, deleteUser } from "@/services/userService";
import { listCompanies } from "@/services/companyService";
import { listBranches } from "@/services/branchService";
import type { User, UserCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { useAuthStore } from "@/store/authStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { SearchInput } from "@/components/ui/SearchInput";
import { StatusBadge, ToneBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { UserFormModal } from "./UserFormModal";

export function UsersPage() {
  const queryClient = useQueryClient();
  const currentUser = useAuthStore((s) => s.user);
  const [search, setSearch] = useState("");
  const [editTarget, setEditTarget] = useState<User | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<User | null>(null);

  const { data: users, isLoading } = useQuery({ queryKey: ["users"], queryFn: listUsers });
  const { data: companies } = useQuery({ queryKey: ["companies"], queryFn: listCompanies });
  const { data: branches } = useQuery({ queryKey: ["branches"], queryFn: () => listBranches() });

  const branchNameById = useMemo(() => {
    const map = new Map<string, string>();
    branches?.forEach((b) => map.set(b.id, b.name));
    return map;
  }, [branches]);

  const createMutation = useMutation({
    mutationFn: (input: UserCreateInput) => createUser(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      toast.success("تم إنشاء المستخدم بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء المستخدم")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: Partial<UserCreateInput> }) => updateUser(id, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteUser(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
      toast.success("تم حذف المستخدم");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف المستخدم")),
  });

  const filtered = useMemo(() => {
    if (!users) return [];
    const q = search.trim().toLowerCase();
    if (!q) return users;
    return users.filter(
      (u) =>
        u.full_name.toLowerCase().includes(q) ||
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q),
    );
  }, [users, search]);

  const columns: Column<User>[] = [
    {
      header: "المستخدم",
      accessor: (u) => (
        <div>
          <div style={{ fontWeight: 600 }}>{u.full_name}</div>
          <div style={{ fontSize: "var(--text-xs)", color: "var(--color-ink-soft)" }} className="ltr-field">
            {u.username} · {u.email}
          </div>
        </div>
      ),
    },
    { header: "الفرع", accessor: (u) => branchNameById.get(u.branch_id) ?? "—" },
    {
      header: "الصلاحية",
      accessor: (u) =>
        u.is_superuser ? (
          <ToneBadge tone="info">
            <ShieldCheck size={12} style={{ marginInlineEnd: 2 }} />
            مدير عام
          </ToneBadge>
        ) : (
          <span style={{ color: "var(--color-ink-soft)", fontSize: "var(--text-sm)" }}>مستخدم</span>
        ),
    },
    { header: "الحالة", accessor: (u) => <StatusBadge active={u.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (u) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(u)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton
            aria-label="حذف"
            variant="danger"
            onClick={() => setDeleteTarget(u)}
            disabled={u.id === currentUser?.id}
            title={u.id === currentUser?.id ? "لا يمكنك حذف حسابك الحالي" : undefined}
          >
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
          title="المستخدمون"
          subtitle="إدارة حسابات المستخدمين وصلاحياتهم"
          actions={
            <Button onClick={() => setCreateOpen(true)} disabled={companyOptions.length === 0}>
              <Plus size={16} />
              مستخدم جديد
            </Button>
          }
        />

        <div style={{ marginBottom: "var(--space-4)" }}>
          <SearchInput value={search} onChange={setSearch} placeholder="بحث بالاسم أو اسم المستخدم أو البريد..." />
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState icon={<UsersIcon size={32} />} title={search ? "لا توجد نتائج مطابقة" : "لا يوجد مستخدمون بعد"} />
        ) : (
          <DataTable columns={columns} rows={filtered} rowKey={(u) => u.id} />
        )}
      </Card>

      <UserFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values as UserCreateInput)}
        submitting={createMutation.isPending}
        title="مستخدم جديد"
        companies={companies ?? []}
        branches={branches ?? []}
      />

      <UserFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل المستخدم"
        initialValues={editTarget ?? undefined}
        companies={companies ?? []}
        branches={branches ?? []}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف المستخدم"
        message={`هل أنت متأكد من حذف "${deleteTarget?.full_name}"؟ لا يمكن التراجع عن هذا الإجراء.`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
