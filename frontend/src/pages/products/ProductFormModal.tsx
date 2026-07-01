import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { FormField } from "@/components/ui/FormField";
import { SelectField } from "@/components/ui/SelectField";
import type { Product, ProductCreateInput } from "@/types/api";

interface ProductFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: ProductCreateInput) => void;
  submitting: boolean;
  title: string;
  initialValues?: Product;
  companyId: string;
  categoryOptions: { value: string; label: string }[];
}

export function ProductFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  title,
  initialValues,
  companyId,
  categoryOptions,
}: ProductFormModalProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProductCreateInput>({
    defaultValues: { is_active: true, company_id: companyId, sale_price: 0, cost_price: 0 },
  });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              company_id: initialValues.company_id,
              category_id: initialValues.category_id,
              name: initialValues.name,
              sku: initialValues.sku ?? "",
              barcode: initialValues.barcode ?? "",
              sale_price: initialValues.sale_price,
              cost_price: initialValues.cost_price,
              is_active: initialValues.is_active,
            }
          : {
              is_active: true,
              company_id: companyId,
              category_id: categoryOptions[0]?.value ?? "",
              sale_price: 0,
              cost_price: 0,
            },
      );
    }
  }, [open, initialValues, reset, companyId, categoryOptions]);

  return (
    <Modal open={open} onClose={onClose} title={title} width={520}>
      <form onSubmit={handleSubmit(onSubmit)} noValidate>
        <FormField
          label="اسم المنتج"
          required
          {...register("name", { required: "اسم المنتج مطلوب" })}
          error={errors.name?.message}
        />

        <SelectField
          label="التصنيف"
          required
          options={categoryOptions}
          placeholder="اختر التصنيف"
          {...register("category_id", { required: "التصنيف مطلوب" })}
          error={errors.category_id?.message}
        />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField label="رمز المنتج (SKU)" ltr {...register("sku")} />
          <FormField label="الباركود" ltr {...register("barcode")} />
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <FormField
            label="سعر البيع"
            type="number"
            step="0.01"
            ltr
            {...register("sale_price", { valueAsNumber: true, min: { value: 0, message: "يجب أن يكون صفرًا أو أكثر" } })}
            error={errors.sale_price?.message}
          />
          <FormField
            label="سعر التكلفة"
            type="number"
            step="0.01"
            ltr
            {...register("cost_price", { valueAsNumber: true, min: { value: 0, message: "يجب أن يكون صفرًا أو أكثر" } })}
            error={errors.cost_price?.message}
          />
        </div>

        <div className="field__checkbox-row">
          <input id="product_is_active" type="checkbox" {...register("is_active")} />
          <label htmlFor="product_is_active">نشط</label>
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
