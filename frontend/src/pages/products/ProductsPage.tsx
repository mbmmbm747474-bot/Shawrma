import { useMemo, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Pencil, Trash2, Boxes } from "lucide-react";
import { listProducts, createProduct, updateProduct, deleteProduct } from "@/services/productService";
import { listCategories } from "@/services/categoryService";
import type { Product, ProductCreateInput } from "@/types/api";
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
import { ProductFormModal } from "./ProductFormModal";

function formatMoney(value: number): string {
  return value.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function ProductsPage() {
  const queryClient = useQueryClient();
  const currentUser = useAuthStore((s) => s.user);
  const [search, setSearch] = useState("");
  const [editTarget, setEditTarget] = useState<Product | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Product | null>(null);

  const { data: products, isLoading } = useQuery({ queryKey: ["products"], queryFn: () => listProducts() });
  const { data: categories } = useQuery({ queryKey: ["categories"], queryFn: listCategories });

  const categoryNameById = useMemo(() => {
    const map = new Map<string, string>();
    categories?.forEach((c) => map.set(c.id, c.name));
    return map;
  }, [categories]);

  const createMutation = useMutation({
    mutationFn: (input: ProductCreateInput) => createProduct(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("تم إنشاء المنتج بنجاح");
      setCreateOpen(false);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل إنشاء المنتج")),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: string; input: ProductCreateInput }) => {
      const { company_id, ...rest } = input;
      return updateProduct(id, rest);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("تم حفظ التعديلات");
      setEditTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حفظ التعديلات")),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteProduct(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] });
      toast.success("تم حذف المنتج");
      setDeleteTarget(null);
    },
    onError: (err) => toast.error(getApiErrorMessage(err, "فشل حذف المنتج")),
  });

  const filtered = useMemo(() => {
    if (!products) return [];
    const q = search.trim().toLowerCase();
    if (!q) return products;
    return products.filter(
      (p) => p.name.toLowerCase().includes(q) || (p.sku ?? "").toLowerCase().includes(q),
    );
  }, [products, search]);

  const columns: Column<Product>[] = [
    {
      header: "المنتج",
      accessor: (p) => (
        <div>
          <div style={{ fontWeight: 600 }}>{p.name}</div>
          {p.sku && (
            <div className="ltr-field" style={{ fontSize: "var(--text-xs)", color: "var(--color-ink-soft)" }}>
              {p.sku}
            </div>
          )}
        </div>
      ),
    },
    { header: "التصنيف", accessor: (p) => categoryNameById.get(p.category_id) ?? "—" },
    { header: "سعر البيع", align: "end", accessor: (p) => <span className="numeric">{formatMoney(p.sale_price)}</span> },
    { header: "سعر التكلفة", align: "end", accessor: (p) => <span className="numeric">{formatMoney(p.cost_price)}</span> },
    { header: "الحالة", accessor: (p) => <StatusBadge active={p.is_active} /> },
    {
      header: "",
      align: "end",
      accessor: (p) => (
        <div className="row-actions">
          <IconButton aria-label="تعديل" onClick={() => setEditTarget(p)}>
            <Pencil size={15} />
          </IconButton>
          <IconButton aria-label="حذف" variant="danger" onClick={() => setDeleteTarget(p)}>
            <Trash2 size={15} />
          </IconButton>
        </div>
      ),
    },
  ];

  const categoryOptions = (categories ?? []).map((c) => ({ value: c.id, label: c.name }));

  if (!currentUser) return <PageSpinner />;

  return (
    <div>
      <Card>
        <CardHeader
          title="المنتجات"
          subtitle="إدارة كتالوج المنتجات"
          actions={
            <Button onClick={() => setCreateOpen(true)} disabled={categoryOptions.length === 0}>
              <Plus size={16} />
              منتج جديد
            </Button>
          }
        />

        {categoryOptions.length === 0 && (
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
            أضف تصنيفًا أولًا قبل إنشاء المنتجات.
          </div>
        )}

        <div style={{ marginBottom: "var(--space-4)" }}>
          <SearchInput value={search} onChange={setSearch} placeholder="بحث بالاسم أو رمز المنتج..." />
        </div>

        {isLoading ? (
          <PageSpinner />
        ) : filtered.length === 0 ? (
          <EmptyState icon={<Boxes size={32} />} title={search ? "لا توجد نتائج مطابقة" : "لا توجد منتجات بعد"} />
        ) : (
          <DataTable columns={columns} rows={filtered} rowKey={(p) => p.id} />
        )}
      </Card>

      <ProductFormModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={(values) => createMutation.mutate(values)}
        submitting={createMutation.isPending}
        title="منتج جديد"
        companyId={currentUser.company_id}
        categoryOptions={categoryOptions}
      />

      <ProductFormModal
        open={Boolean(editTarget)}
        onClose={() => setEditTarget(null)}
        onSubmit={(values) => editTarget && updateMutation.mutate({ id: editTarget.id, input: values })}
        submitting={updateMutation.isPending}
        title="تعديل المنتج"
        initialValues={editTarget ?? undefined}
        companyId={currentUser.company_id}
        categoryOptions={categoryOptions}
      />

      <ConfirmDialog
        open={Boolean(deleteTarget)}
        title="حذف المنتج"
        message={`هل أنت متأكد من حذف "${deleteTarget?.name}"؟`}
        confirmLabel="حذف"
        loading={deleteMutation.isPending}
        onConfirm={() => deleteTarget && deleteMutation.mutate(deleteTarget.id)}
        onCancel={() => setDeleteTarget(null)}
      />
    </div>
  );
}
