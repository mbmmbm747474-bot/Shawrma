import { useEffect } from "react";
import { useFieldArray, useForm } from "react-hook-form";
import { Plus, Trash2 } from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { IconButton } from "@/components/ui/IconButton";
import { FormField } from "@/components/ui/FormField";
import { SelectField } from "@/components/ui/SelectField";
import type { Product, PurchaseOrder, PurchaseOrderCreateInput, Supplier } from "@/types/api";

interface PurchaseOrderFormValues {
  supplier_id: string;
  branch_id: string;
  discount: number;
  tax: number;
  items: { product_id: string; quantity: number; unit_cost: number }[];
}

interface PurchaseOrderFormModalProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (values: PurchaseOrderCreateInput) => void;
  submitting: boolean;
  suppliers: Supplier[];
  products: Product[];
  branchOptions: { value: string; label: string }[];
  initialValues?: PurchaseOrder;
}

export function PurchaseOrderFormModal({
  open,
  onClose,
  onSubmit,
  submitting,
  suppliers,
  products,
  branchOptions,
  initialValues,
}: PurchaseOrderFormModalProps) {
  const isEdit = Boolean(initialValues);

  const {
    register,
    handleSubmit,
    reset,
    control,
    watch,
    formState: { errors },
  } = useForm<PurchaseOrderFormValues>({
    defaultValues: {
      discount: 0,
      tax: 0,
      branch_id: branchOptions[0]?.value ?? "",
      items: [{ product_id: "", quantity: 1, unit_cost: 0 }],
    },
  });

  const { fields, append, remove } = useFieldArray({ control, name: "items" });

  useEffect(() => {
    if (open) {
      reset(
        initialValues
          ? {
              supplier_id: initialValues.supplier_id,
              branch_id: initialValues.branch_id,
              discount: initialValues.discount,
              tax: initialValues.tax,
              items: initialValues.items.map((i) => ({
                product_id: i.product_id,
                quantity: i.quantity,
                unit_cost: i.unit_cost,
              })),
            }
          : {
              discount: 0,
              tax: 0,
              branch_id: branchOptions[0]?.value ?? "",
              items: [{ product_id: "", quantity: 1, unit_cost: 0 }],
            },
      );
    }
  }, [open, initialValues, reset, branchOptions]);

  const watchedItems = watch("items");
  const watchedDiscount = watch("discount") || 0;
  const watchedTax = watch("tax") || 0;
  const subtotal = (watchedItems ?? []).reduce(
    (sum, item) => sum + (Number(item.quantity) || 0) * (Number(item.unit_cost) || 0),
    0,
  );
  const total = subtotal - Number(watchedDiscount) + Number(watchedTax);

  const productOptions = products.map((p) => ({ value: p.id, label: p.sku ? `${p.name} (${p.sku})` : p.name }));
  const supplierOptions = suppliers.map((s) => ({ value: s.id, label: s.name }));

  function handleFormSubmit(values: PurchaseOrderFormValues) {
    onSubmit({
      supplier_id: values.supplier_id,
      branch_id: values.branch_id,
      discount: Number(values.discount) || 0,
      tax: Number(values.tax) || 0,
      items: values.items.map((i) => ({
        product_id: i.product_id,
        quantity: Number(i.quantity),
        unit_cost: Number(i.unit_cost),
      })),
    });
  }

  return (
    <Modal open={open} onClose={onClose} title={isEdit ? "تعديل أمر الشراء" : "أمر شراء جديد"} width={720}>
      <form onSubmit={handleSubmit(handleFormSubmit)} noValidate>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)" }}>
          <SelectField
            label="المورد"
            required
            options={supplierOptions}
            placeholder="اختر المورد"
            {...register("supplier_id", { required: "المورد مطلوب" })}
            error={errors.supplier_id?.message}
          />
          <SelectField
            label="الفرع"
            required
            options={branchOptions}
            placeholder="اختر الفرع"
            disabled={isEdit}
            {...register("branch_id", { required: "الفرع مطلوب" })}
            error={errors.branch_id?.message}
          />
        </div>

        <div style={{ marginTop: "var(--space-2)", marginBottom: "var(--space-2)" }}>
          <p className="field__label" style={{ marginBottom: "var(--space-2)" }}>
            بنود الطلب
          </p>

          {fields.map((field, index) => (
            <div
              key={field.id}
              style={{
                display: "grid",
                gridTemplateColumns: "2fr 1fr 1fr auto",
                gap: "var(--space-2)",
                alignItems: "start",
                marginBottom: "var(--space-2)",
              }}
            >
              <SelectField
                label={index === 0 ? "المنتج" : ""}
                options={productOptions}
                placeholder="اختر المنتج"
                {...register(`items.${index}.product_id`, { required: "مطلوب" })}
                error={errors.items?.[index]?.product_id?.message}
              />
              <FormField
                label={index === 0 ? "الكمية" : ""}
                type="number"
                step="0.001"
                ltr
                {...register(`items.${index}.quantity`, {
                  valueAsNumber: true,
                  required: "مطلوب",
                  min: { value: 0.001, message: "> 0" },
                })}
                error={errors.items?.[index]?.quantity?.message}
              />
              <FormField
                label={index === 0 ? "تكلفة الوحدة" : ""}
                type="number"
                step="0.01"
                ltr
                {...register(`items.${index}.unit_cost`, {
                  valueAsNumber: true,
                  required: "مطلوب",
                  min: { value: 0, message: ">= 0" },
                })}
                error={errors.items?.[index]?.unit_cost?.message}
              />
              <div style={{ paddingTop: index === 0 ? "26px" : 0 }}>
                <IconButton
                  type="button"
                  aria-label="حذف البند"
                  variant="danger"
                  onClick={() => fields.length > 1 && remove(index)}
                  disabled={fields.length <= 1}
                >
                  <Trash2 size={15} />
                </IconButton>
              </div>
            </div>
          ))}

          <Button
            type="button"
            variant="ghost"
            size="sm"
            onClick={() => append({ product_id: "", quantity: 1, unit_cost: 0 })}
          >
            <Plus size={14} />
            إضافة بند
          </Button>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "var(--space-4)", marginTop: "var(--space-4)" }}>
          <FormField
            label="الخصم"
            type="number"
            step="0.01"
            ltr
            {...register("discount", { valueAsNumber: true, min: 0 })}
          />
          <FormField label="الضريبة" type="number" step="0.01" ltr {...register("tax", { valueAsNumber: true, min: 0 })} />
        </div>

        <div
          style={{
            background: "var(--color-paper)",
            borderRadius: "var(--radius-md)",
            padding: "var(--space-4)",
            marginTop: "var(--space-2)",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "var(--text-sm)", color: "var(--color-ink-soft)" }}>
            <span>الإجمالي الفرعي</span>
            <span className="numeric">{subtotal.toFixed(2)}</span>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 700, fontSize: "var(--text-lg)", marginTop: "var(--space-1)" }}>
            <span>الإجمالي النهائي</span>
            <span className="numeric">{total.toFixed(2)}</span>
          </div>
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
