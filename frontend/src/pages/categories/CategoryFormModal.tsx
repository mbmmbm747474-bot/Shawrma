import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import type { ProductCategory, ProductCategoryCreateInput } from "@/types/api";

interface CategoryFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: ProductCategoryCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: ProductCategory;
  companyId: string;
}

export function CategoryFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  companyId,
}: CategoryFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProductCategoryCreateInput>({ defaultValues: { is_active: true, company_id: companyId } });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              company_id: initialValues.company_id,
              name: initialValues.name,
              description: initialValues.description ?? "",
              is_active: initialValues.is_active,
            }
          : { is_active: true, company_id: companyId },
      );
    }
  }, [open, initialValues, reset, companyId]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={460}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <FormField
          label="اسم التصنيف"
          required
          {...register("name", { required: "اسم التصنيف مطلوب" })}
          error={errors.name?.message}
        />
        <FormField label="الوصف" {...register("description")} />

        <div className="field__checkbox-row">
          <input id="category_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="category_is_active">نشط</label>
        </div>

        <div style={{ display: "flex", gap: "var(--space-3)", justifyContent: "flex-end", marginTop: "var(--space-5)" }}>
          <Button type="button" variant="ghost" onClick={onClose} disabled={submitting}>
            إلغاء
          </Button>
          <Button type="submit" loading={submitting}>
            حفظ
          </Button>
        </div>
      </form>
    </Modal>
  );
}
