import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, FolderTree } from "lucide-react";
import { listCategories, createCategory, updateCategory, deleteCategory } from "@/services/categoryService";
import type { ProductCategory, ProductCategoryCreateInput } from "@/types/api";
import { getApiErrorMessage } from "@/services/apiClient";
import { toast } from "@/store/toastStore";
import { useAuthStore } from "@/store/authStore";
import { Card, CardHeader } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { DataTable, type Column } from "@/components/ui/DataTable";
import { StatusBadge } from "@/components/ui/StatusBadge";
import { PageSpinner, EmptyState } from "@/components/ui/EmptyState";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { CategoryFormModal } from "./CategoryFormModal";

export function CategoriesPage() {
  const queryClient = useQueryClient();
  const currentUser = useAuthStore((s) => s.user);
  const [editTarget, setEditTarget] = useState<ProductCategory | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<ProductCategory | null>(null);

  const { data: categories, isLoading } = useQuery({ queryKey: ["categories"], queryFn: listCategories });

  const createMutation = useMutation({
    mutationFn: (input: ProductCategoryCreateInput) => createCategory(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
      toast.success("تم إنشاء التصنيف بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء التصنيف")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: ProductCategoryCreateInput }) => {
      const { company_id, ...rest } = input;
      return updateCategory(id, rest);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteCategory(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["categories"] });
      toast.success("تم حذف التصنيف");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف التصنيف")),
  });

  const columns: Column<ProductCategory>[] = [
    { header: "التصنيف", accessor: (c) => <span style={{ fontWeight: 600 }}>{c.name}</span> },
    { header: "الوصف", accessor: (c) => c.description ?? "—" },
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

  if (!currentUser) return <PageSpinner />;

  return (
    <div>
      <Card>
        <CardHeader
          title="تصنيفات المنتجات"
          subtitle="تنظيم المنتجات في تصنيفات"
          actions={
            <Button onClick={() => setCreateOpen(true)}>
              <Plus size={16} />
              تصنيف جديد
            </Button>
          }
        />

        {isLoading ? (
          <PageSpinner />
        ) : !categories || categories.length === 0 ? (
          <EmptyState icon={<FolderTree size={32} />} title="لا توجد تصنيفات بعد" />
        ) : (
          <DataTable columns={columns} rows={categories} rowKey={(c) => c.id} />
        )}
      </Card>

      <CategoryFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="تصنيف جديد"
        companyId={currentUser.company_id}
      />

      <CategoryFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل التصنيف"
        initialValues={editTarget ?? undefined}
        companyId={currentUser.company_id}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف التصنيف"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
